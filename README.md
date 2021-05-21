# README

Run the site locally for development

For production deployment configuration, refer to [Deployment README](deployment/README.md)

## Prerequisites

- Python 3

## Quick Start Guide

Assuming root directory is the repo directory for every start of the scripts sections.

Create a virtual environment for development purposes

Linux
```shell script
python3 -m venv virtualenv
source virtualenv/bin/activate
```

Windows
```shell script
python -m venv sagta_env
.\sagta_env\Scripts\activate.bat
```

Install dependencies for development

```shell script
pip install -r requirements.txt -r requirements.dev.txt
or
pip3 install --user -r requirements.txt -r requirements.dev.txt
```

Uncomment the DEBUG section in urls.py

Run initial manage.py command

```shell script
python manage.py migrate
python manage.py collectstatic
```

Start Django web development server

```shell script
python manage.py runserver 0.0.0.0:8080
```

Create Super User

``` shell script
python manage.py createsuperuser
```

Web development server will available at http://localhost:8080