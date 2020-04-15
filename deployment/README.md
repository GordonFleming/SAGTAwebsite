# Deployment README

This is a guide to start deployment configuration for production instance using docker and docker-compose.

## Prerequisite

- Docker Engine
- Resolvable FQDN to be used as SITE_NAME

## Quick Start Guide

These steps will deploy production server on a host with docker installed.
Every shell script command is assumed to start from this `deployment` directory.

### Create configurations

Create a copy of docker-compose environment file:

```shell script
cp .env.prod.example .env
```

Modify the settings inside `.env` file to reflect production configurations.
Change `SITE_NAME` and `HTTP_PORT` to reflect real FQDN name and port that 
the server will host (if it is under load balancer/reverse proxy).
For a production site, generate a random string for `SECRET_KEY` value.

Create a copy of nginx config file:

```shell script
cp nginx.prod.conf nginx.conf
```

Modify nginx configuration inside `nginx.conf` file to reflect nginx reverse proxy 
settings.
Nginx is used to reverse proxy `SITE_NAME` into `uwsgi` container that runs gunicorn.
Nginx is also used to serve file based requests directly like static and media folder.
Change the `server_name` directive to reflect the FQDN or IP Address that is going to be used.

Create a copy of docker-compose.override.yml file:

```shell script
cp docker-compose.override.sample.yml docker-compose.override.yml
```

This file is used to easily modify docker-compose configuration if you need it.

### Preparing docker image

Build the image if you haven't already, or alternatively, pull the image from image registry.
Pick either one.

#### Building the image directly

Run make build

```shell script
make build
```

This will build the image and tag it locally as sagtaweb:latest.
You may want to tag it as different version (for history versioning) like this:

```shell script
docker tag sagtaweb:latest sagtaweb:<YY.MM.DD>
```

With <YY.MM.DD> replaced by current year, month, and date, like this: 20.04.18
That way, even if you rebuild you will have previous tag (locally) in the machine.

#### Pulling the image from registry

If you pull the image from docker image registry, then you don't need to build.
Modify `docker-compose.override.yml` like this:

```yaml
version: '3.7'
services:
  uwsgi:
    image: <DOCKER_HUB_USER_NAME>/<REPO_NAME>:<TAG_NAME>
```

Note, that we deleted `build` key because we don't want to build the image.
Change `<DOCKER_HUB_USER_NAME>/<REPO_NAME>:<TAG_NAME>` with the full name of the image version.
It will be something along like this: `wolfbyne/sagtaweb:20.04.18`

Then run:

```shell script
make pull
```

### Running the service

To run the service:

```shell script
make up
```

To shut it down, run:

```shell script
make down
```


