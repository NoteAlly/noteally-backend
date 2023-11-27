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

# Docker

### Build image

```bash
docker build -t noteally-backend .
```

```bash
docker build -t noteally-backend --progress=plain --no-cache . --build-arg ENV_FILE=.env
```

By using `--progress=plain` we can see the progress of the build. By using `--no-cache` we can avoid using the cache.
This is useful because, for example if we want to check the folder structure of the image, we can use

```docker
RUN ls
```

and we can see the output of the command.

### Run container

```bash
docker run -p 8000:8000 --name noteally-backend_app noteally-backend
```

### Run container in background

```bash
docker run -d -p 8000:8000 --name noteally-backend_app noteally-backend
```

### Run container with volume

```bash
docker run -d -p 8000:8000 -v src:/drf_src --name noteally-backend_app noteally-backend
```

### Run container with environment variables

```bash
docker run -d -p 8000:8000 --name noteally-backend_app \
                    -e environment_var_1='foo' \
                    -e environment_var_2='bar' \
                    -e environment_var_i='car' \
                    noteally-backend
```

### Run container with environment variables from file

```bash
docker run -d -p 8000:8000 --name noteally-backend_app --env-file .env noteally-backend
```

### Stop container

```bash
docker stop noteally-backend_app
```

### Start container

```bash
docker start noteally-backend_app
```

### Remove container

```bash
docker rm noteally-backend_app
```

### Remove images

```bash
docker rmi noteally-backend <image-2> <image-3> ...
```

### Remove images with pattern

```bash
docker rmi $(docker images --format '{{.Repository}}:{{.Tag}}' | grep 'noteally')
```

### Save image

```bash
docker save -o noteally-backend.tar noteally-backend
```

or
  
```bash
docker save noteally-backend > noteally-backend.tar
```

### Load image

```bash
docker load -i noteally-backend.tar
```

or

```bash
docker load < noteally-backend.tar
```
