import io

import requests
from django.conf import settings

from imageuploader.imageuploader import image_uploader


def download_file(url):
    # stream response, so we dont have to keep large files in memory
    file_object = requests.get(url, stream=True, timeout=1)

    result = io.BytesIO()
    # write file, being streamed from file server
    for chunk in file_object.iter_content(chunk_size=1048576):
        result.write(chunk)
    return result


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
