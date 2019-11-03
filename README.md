## Docker

- set required environment variables

  ```bash
    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=
    export AWS_REGION=
    export S3_BUCKET_NAME=
    export MEM_DB_HOST=
    export MEM_DB_PORT=
    export MEM_DB_PASSWORD=
  ```

  #### NB

  If you choose to cache onto a remote redis server, please set the `MEM_DB_HOST`, `MEM_DB_PORT` and `MEM_DB_PASSWORD` variables to the remote credentials. But if you rely on the redis container run by the docker compose file, you are not required to set `MEM_DB_HOST`, `MEM_DB_PORT` and `MEM_DB_PASSWORD` variables, as they have valid defaults set in the docker compose file.

- start service

  ```bash
  docker-compose up
  ```

The API should now bw available at `http://localhost/api/v1`.

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
    export MEM_DB_HOST=
    export MEM_DB_PORT=
    export MEM_DB_PASSWORD=
  ```

- run server

  ```bash
  python manage.py runserver
  ```

The API should now bw available at `http://localhost:8000/api/v1`.

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

- Error `500` (sorry, service is temporarily unavailable): A 500 error from the api signifies invalid or missing configuration. Please check that the environment variables are set and accurate.

- Error `424` (failure in reaching server): A 424 error from the api signifies a failure to reach the provided url. This failure could be due to internet connectivity downtime on the machine or downtime at the host of the provided image.
