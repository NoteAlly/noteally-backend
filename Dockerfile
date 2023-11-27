# Use official Python runtime as a parent image
FROM python:3.11.4

# Load Variables
# ARG variable are only available during the build process while ENV variables are also available in the container

ENV DJANGO_KEY=$DJANGO_KEY
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME
ENV AWS_DEFAULT_ACL=$AWS_DEFAULT_ACL
ENV AWS_S3_REGION_NAME=$AWS_S3_REGION_NAME
ENV AWS_COGNITO_DOMAIN=$AWS_COGNITO_DOMAIN


RUN git clone -b NOTE-112-dockerize-rest-api https://github.com/NoteAlly/noteally-backend.git /drf_src
# COPY . /drf_src

WORKDIR /drf_src

# Setting PYTHONUNBUFFERED=1 allows for log messages to be immediately dumped to the stream instead of being buffered.
# This is useful for receiving timely log messages and avoiding situations where the application crashes without emitting a relevant message.
ENV PYTHONUNBUFFERED 1

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# Create a .env file with the environment variables and run the development server
CMD echo "DJANGO_KEY=$DJANGO_KEY" >> .env; \
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> .env; \
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env; \
    echo "AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME" >> .env; \
    echo "AWS_DEFAULT_ACL=$AWS_DEFAULT_ACL" >> .env; \
    echo "AWS_S3_REGION_NAME=$AWS_S3_REGION_NAME" >> .env; \
    echo "AWS_COGNITO_DOMAIN=$AWS_COGNITO_DOMAIN" >> .env; \
    python3 manage.py makemigrations --settings=NoteAlly.development_settings; \
    python3 manage.py migrate --run-syncdb --settings=NoteAlly.development_settings; \
    python manage.py runserver 0.0.0.0:8000 --settings=NoteAlly.development_settings
    # python3 manage.py makemigrations --settings=NoteAlly.production_settings; \
    # python3 manage.py migrate --run-syncdb --settings=NoteAlly.production_settings; \
    # python manage.py runserver 0.0.0.0:8000 --settings=NoteAlly.production_settings