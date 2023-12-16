# Noteally Backend - Services

This repository contains the backend services for the Noteally application. These services are:

- Authentication service (auth-service)
- User service (user-service)
- Tutor service (tutor-service)
- Material service (material-service)
- Information service (info-service)

The authentication service guarantees authorization and authentication for the other services. This service interacts with a cognito user pool and a cognito identity pool.

The user service provides CRUD operations for users. It also provides endpoints that allow users to subscribe to tutors and to get a list of subscribed tutors.

Similar to the user service, the tutor service provides CRUD operations for tutors. It also provides endpoints that allow access to tutors' materials and information.

The material service is responsible for CRUD operations for materials, allowing tutors to upload and delete materials. This service also implements endpoints that allow users to download and rate materials.

The information service provides and manages general information about the application, such as the universities and study areas.


## Run a service

### Setup database

```bash
python3 manage.py makemigrations --settings=NoteAlly.development_settings
python3 manage.py migrate --run-syncdb --settings=NoteAlly.development_settings
```

### Run server in development mode

```bash
python3 manage.py runserver --settings=NoteAlly.development_settings
```

### Run server in production mode

```bash
python3 manage.py runserver --settings=NoteAlly.production_settings
```

### Run tests

```bash
python3 manage.py test --settings=NoteAlly.test_settings
```

### Create superuser

```bash
python manage.py createsuperuser   
```

## Docker

### Build an image of a service

```bash
docker build -t noteally-service-image .
```

### Run container

Create a container with environment variables

```bash
docker run -d -p 8000:8000 --name noteally-service \
                    -e DJANGO_KEY=... \
                    -e AWS_ACCESS_KEY_ID=... \
                    -e AWS_SECRET_ACCESS_KEY=... \
                    ...
                    noteally-service-image
```

Create a container with environment variables from a file

```bash
docker run -d -p 8000:8000 --name noteally-service --env-file .env noteally-service-image
```

### Stop container

```bash
docker stop noteally-service
```

### Remove container

```bash
docker rm noteally-service
```

### Remove image

```bash
docker rmi noteally-service-image
```
