# wilber-web
Gimp Assets Sharing Server

# How to run django on linux:

Install system dependency:

```bash
apt install virtualenvwrapper
```
Create a virtualenv with Python3 and install dependencies:

```bash
mkvirtualenv wilber -p /usr/bin/python3

pip install -r wilber-web/wilber/requirements/base.txt
```
Create django database and the admin user:


```bash
cd wilber-web/wilber

cp .env.example .env

python manage.py migrate

python manage.py createsuperuser --username admin --email admin@wilber.org
```

Run deveploment server:

```bash
python manage.py runserver
```

go to http://127.0.0.1:8000/admin and populate the database with some assets

go to http://127.0.0.1:8000 and see it working!
