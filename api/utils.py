import io
import os
import uuid

import requests
from django.conf import settings

from imageuploader.imageuploader import image_uploader


def download_file(url):
    # downloads file in url and retuns as a BytesIO object

    # stream response, so we dont have to keep large files in memory
    r = requests.get(url, stream=True, timeout=5)

    temp_file_name = f"temp/{str(uuid.uuid4())}.tmp"

    """
    write stream in chunks of 1MB to file on disk to prevent hogging
    the memory during the duration of download.
    """  
    with open(temp_file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1048576): 
            f.write(chunk)

    # after download, read the file from disk into a BytesIO file object in memory
    with open(temp_file_name, 'rb') as f:
        file_object = io.BytesIO(f.read())

    # clean up. remove file from disk
    os.remove(temp_file_name)

    return file_object


def generate_s3_path(filename):
    return f"https://mines-img-upload.s3.amazonaws.com/{filename}"


def get_image_handler():
    aws_credentials = {
        "access_key_id": settings.AWS_ACCESS_KEY_ID,
        "bucket_name": settings.S3_BUCKET_NAME,
        "secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        "region": settings.AWS_REGION,
    }
    image_handler = ImageHandler(
        aws_credentials,
        settings.IMAGE_MAX_WIDTH,
        settings.IMAGE_MAX_HEIGHT,
        min_width=settings.IMAGE_MIN_WIDTH,
        min_height=settings.IMAGE_MIN_HEIGHT,
        mem_db_host=settings.MEM_DB_HOST,
        mem_db_port=settings.MEM_DB_PORT,
        mem_db_password=settings.MEM_DB_PASSWORD,
    )
    return image_handler


def upload(image_url):

    # download image file object
    file_object = download_file(image_url)

    # instantiate image handler
    image_handler = get_image_handler()

    # validate image
    image_handler.validate(file_object)

    # upload image
    file_name = image_handler.upload()
    uploaded_image_url = generate_s3_path(file_name)

    # discard image object
    image_handler.close()

    return uploaded_image_url


class ImageHandler(image_uploader.ImageUploader):
    def validate(self, file_object):
        self.image_object = file_object
        self._validate()

    def upload(self):
        self._upload_to_server()
        return self.file_name
