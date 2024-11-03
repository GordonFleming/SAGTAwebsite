FROM python:3.12-slim

# For python logs
ENV PYTHONUNBUFFERED=1 \
    UWSGI_PORT=8000

# Create a non-root user and group called wagtail
RUN groupadd -r wagtail && useradd -r -g wagtail wagtail

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
        build-essential \
        libpq-dev \
        gettext \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Create application directory and set permissions
RUN mkdir -p /usr/src/app \
    && chown -R wagtail:wagtail /usr/src/app

WORKDIR /usr/src/app

# Copy the requirements file and install Python dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt \
    && rm -f /usr/src/app/requirements.txt

# Install Gunicorn as part of the Python dependencies
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY --chown=wagtail:wagtail . /usr/src/app

# Change to non-root user
USER wagtail

# Expose the UWSGI port
EXPOSE ${UWSGI_PORT}

# Set the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Command to run Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind=0.0.0.0:${UWSGI_PORT}", "--workers=4"]
