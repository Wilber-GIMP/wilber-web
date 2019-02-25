# wilber-web
Gimp Assets Sharing Server

# How to run django on linux:

Install system dependency:
`apt install virtualenvwrapper`

Create a virtualenv with Python3 and install dependencies:
`mkvirtualenv wilber -p /usr/bin/python3
pip install -r wilber-web/wilber/requirements/base.txt`

Create django database and the admin user:
`cd wilber-web/wilber
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@wilber.org
`

Run deveploment server:

`python manage.py runserver
`

go to http://127.0.0.1:8000/admin and populate the database with some assets

go to http://127.0.0.1:8000 and see it working!
