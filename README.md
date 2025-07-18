# README

Run the site locally for development

## Prerequisites

- Python 3

## Quick Start Guide

Assuming root directory is the repo directory for every start of the scripts sections.

Create a virtual environment for development purposes

Linux
```shell script
python3 -m venv virtualenv / virtualenv -p python3 yourVenv
source virtualenv/bin/activate
```

Install dependencies for development

```shell script
pip install -r requirements.txt -r requirements.dev.txt
```

### Make sure .env is configured

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

Add the cron jobs
``` shell script
python manage.py crontab add
```

Web development server will available at http://localhost:8080
