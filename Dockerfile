FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# For python logs
ENV PYTHONUNBUFFERED=1
# Compile bytecode
ENV UV_COMPILE_BYTECODE=1
# Reference the virtualenv
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

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
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libmagic1 \
    libjpeg-dev \
    zlib1g-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Litestream for SQLite replication
RUN wget -q https://github.com/benbjohnson/litestream/releases/download/v0.5.6/litestream-0.5.6-linux-arm64.tar.gz \
    && tar -xzf litestream-0.5.6-linux-arm64.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/litestream \
    && rm litestream-0.5.6-linux-arm64.tar.gz

# Create application directory
WORKDIR /usr/src/app

# Install dependencies using uv
# Sync the project into a new environment, using the frozen lockfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . /usr/src/app

# Expose the UWSGI port
EXPOSE 80

# Set the entrypoint script
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Command to run Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind=0.0.0.0:80", "--workers=2", "--threads=4", "--timeout=60"]