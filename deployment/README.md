# Deployment README

This is a guide to start deployment configuration for production instance using docker and docker-compose.

## Quick Start Guide

These steps will deploy production server on a host with docker installed.
Every shell script command is assumed to start from this `deployment` directory.


### Prerequisite

- Docker Engine
- Resolvable FQDN to be used as SITE_NAME

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

We can push the docker image into public registry like this:

```
docker push <DOCKER_HUB_USER_NAME>/<REPO_NAME>:<TAG_NAME>
```

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


## Rancher Deployment Guide

### Prerequisite

- Rancher v1.6 with host configured

### Create configuration

Copy and create configuration from `docker-compose.prod.yml` (new name for the file is arbitrary).
All the values needed to generate the website **must** be hardcoded here.

Some important keys:

|  Key   |   Description   |   Sample value   |
|--------|-----------------|------------------|
| services.wsgi.environment.SECRET_KEY | Put any long random string | "kajhgkjahjkshaf98qh-0q-ut31qwiakhewqioxmuwmiotgynnp" |
| services.wsgi.environment.SITE_NAME | Put FQDN for the production site | "sagta.org.za" |
| services.rsync.environment.SSH_AUTH_KEY_1 | Put your SSH **public** key | "ssh-rsa AAAAAAAA user@email.org" |

Copy and create configuration from `nginx.prod.con` as `mysite.conf`.
Replace the server_name directive with the server's FQDN.

### Generate Rancher Stack

In Rancher, on the Stacks UI, click Add Stack.
Fill in the stack name, and copy paste the content of `docker-compose.prod.yml` that you configured previously.
Create the stack and wait for the service to complete.

### Copy/Migrate production data

If you already put your ssh public key, you can rsync into your server using port 522.

Several files that needs to be copied:

| File | Usage |
|------|-------|
| media/ | Media folder |
| mysite.conf | Your site's nginx configuration |
| db.sqlite3 | Your sqlite's database |

Copy these content into the server:

Execute it from root repo:

```shell script
rsync -avzP -e 'ssh -p 522' media/* root@sagta.org.za:/media
rsync -avzP -e 'ssh -p 522' db.sqlite3 root@sagta.org.za:/db/db.sqlite3
rsync -avzP -e 'ssh -p 522' deployment/mysite.conf root@sagta.org.za:/nginx/conf.d/mysite.conf
```

You can replace `sagta.org.za` with IP address of the machine if it is behind a proxy

### Check folder permissions

Wagtail container run as user Wagtail. Check that the folder permission is sufficient for 
sqlite database and media folder.

Go inside wsgi container (from Rancher, there's no other way), and check wagtail's UID:

```shell script
cat /etc/passwd | grep wagtail
```

The third column is the UID. In this case, usually ID: 1000.

Go inside our rsync server container and set appropriate permissions:

```shell script
ssh -p 522 root@sagta.org.za
# from inside the shell of rsync server
chown -R 1000:1000 /media /db /static
```

Alternatively you could use Rancher shell of rsync server to do this.


### Restart services

Restart `wsgi` and `nginx` service to apply latest changes.

### Expose nginx service

`nginx` service acts as the server. Expose this service to the internet.
Either expose ports 80 of `nginx` server directly to the host machine via Rancher interface,
or alternatively use Rancher load balancer.
