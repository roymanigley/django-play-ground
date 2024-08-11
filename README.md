# Django-Play-Ground
> Django project for experiments containting a movie retail database

## usage

### initial setup
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirenemts.txt
./manage.py migrate
./manage.py loaddata data.json.gz
./manage.py createsuperuser
```

### run the service

```
./manage.py runserver
```
