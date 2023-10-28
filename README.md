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
