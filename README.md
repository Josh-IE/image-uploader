## Docker

- set environment variables

  ```bash
    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=
    export AWS_REGION=
    export S3_BUCKET_NAME=
  ```

- start service

  ```bash
  docker-compose up
  ```

The API should now bw available at http://localhost:80/api/v1.

## Terminal

### Setup

- install requirements

  ```bash
  pip install -r requirements.txt -r imageuploader/requirements.txt
  ```

- set environment variables

  ```bash
    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=
    export AWS_REGION=
    export S3_BUCKET_NAME=
  ```

- run server

  ```bash
  python manage.py runserver
  ```

The API should now bw available at http://localhost:8000/api/v1.

## API

### Endpoints

`/image/upload/`
POST: Returns the url of the uploaded image.

#### params

- image_url: (string) url of the image to be uploaded.

#### request data

```json
{
  "image_url": "https://i.imgur.com/n5pofy8.jpg"
}
```

#### response data

```json
{
  "image_url": "https://mines-img-upload.s3.amazonaws.com/9a5ecb73-7602-4440-a29b-fc15a55f0e9a.jpeg"
}
```

### Troubleshooting

- Error 500: A 500 error from the api signifies invalid or missing configuration. Please check that the environment variables are set and accurate.
