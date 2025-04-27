FROM python:3.12-slim

# For python logs
ENV PYTHONUNBUFFERED=1

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
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ofelia for job scheduling
RUN wget -q https://github.com/mcuadros/ofelia/releases/download/v0.3.7/ofelia_0.3.7_linux_amd64.tar.gz \
    && tar -xzf ofelia_0.3.7_linux_amd64.tar.gz \
    && mv ofelia /usr/local/bin/ \
    && chmod +x /usr/local/bin/ofelia \
    && rm ofelia_0.3.7_linux_amd64.tar.gz

# Create application directory and set permissions
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# Copy the requirements file and install Python dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt \
    && rm -f /usr/src/app/requirements.txt

# Install Gunicorn as part of the Python dependencies
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . /usr/src/app

# Expose the UWSGI port
EXPOSE 80

# Set the entrypoint script
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Command to run Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind=0.0.0.0:80", "--workers=4"]
