# noteally-backend

## Setup database

```bash
python3 manage.py makemigrations --settings=NoteAlly.development_settings
python3 manage.py migrate --run-syncdb --settings=NoteAlly.development_settings
```

## Run server in development mode

```bash
python3 manage.py runserver --settings=NoteAlly.development_settings
```

## Run server in production mode

```bash
python3 manage.py runserver --settings=NoteAlly.production_settings
```

## Run tests

```bash
python3 manage.py test --settings=NoteAlly.test_settings
```

## Create superuser

```bash
python manage.py createsuperuser   
```

## Docker

### Build image

```bash
docker build -t noteally-backend .
```

### Run container

#### Run container with environment variables

```bash
docker run -d -p 8000:8000 --name noteally-backend_app \
                    -e DJANGO_KEY=... \
                    -e AWS_ACCESS_KEY_ID=... \
                    -e AWS_SECRET_ACCESS_KEY=... \
                    ...
                    noteally-backend
```

#### Run container with environment variables from file

```bash
docker run -d -p 8000:8000 --name noteally-backend_app --env-file .env noteally-backend
```

### Stop container

```bash
docker stop noteally-backend_app
```

### Remove container

```bash
docker rm noteally-backend_app
```

### Remove image

```bash
docker rmi noteally-backend <image-2> <image-3> ...
```
