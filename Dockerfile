FROM python:3.10-slim-buster

# For python logs
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y tzdata \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    && apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
 
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

COPY . /usr/src/app

RUN useradd wagtail
RUN chown -R wagtail /usr/src/app
USER wagtail
 
ENV UWSGI_PORT 8000

EXPOSE ${UWSGI_PORT}
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
 
CMD gunicorn mysite.wsgi:application --bind 0.0.0.0:${UWSGI_PORT} --workers 3