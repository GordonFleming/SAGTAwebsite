# README

Run the site locally for development

For production deployment configuration, refer to [Deployment README](deployment/README.md)

## Prerequisites

- Python 3

## Quick Start Guide

Assuming root directory is the repo directory for every start of the scripts sections.

Create a virtual environment for development purposes

```shell script
virtualenv env
source env/bin/activate
```

Install dependencies for development

```shell script
pip install -r requirements.txt -r requirements.dev.txt
```

Uncomment the DEBUG section in urls.py

Run initial manage.py command

```shell script
./manage.py migrate
./manage.py collectstatic
```

Start Django web development server

```shell script
./manage.py runserver 0.0.0.0:8080
```

Web development server will available at http://localhost:8080
