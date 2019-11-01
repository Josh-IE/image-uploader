FROM python:3

WORKDIR /code

# Install requirements
COPY requirements.txt /code/
COPY imageuploader/requirements.txt /code/requirements-ext.txt

RUN pip install -r requirements.txt -r requirements-ext.txt

COPY . /code