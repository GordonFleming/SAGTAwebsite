# Use an official Python runtime as a parent image
FROM python:3.9
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

ENV UWSGI_PORT 8000

EXPOSE ${UWSGI_PORT}
ENTRYPOINT ["/code/entrypoint.sh"]


CMD gunicorn mysite.wsgi:application --bind 0.0.0.0:${UWSGI_PORT} --workers 3
