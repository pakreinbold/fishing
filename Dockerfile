# Submit to Google Cloud using `gcloud builds submit --tag IMAGE_URL`
# Where IMAGE_URL has structure LOCATION-docker.pkg.dev/PROJECT_ID/REPO_NAME/PATH:TAG
# More info: https://cloud.google.com/run/docs/building/containers#use-dockerfile

# lightweight Python base image
FROM python:3.10-slim

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies needed by poetry and project
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install a fixed version of poetry
ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python3 - --version "$POETRY_VERSION"

# Create a working directory
WORKDIR /app

# Install project and its dependencies
COPY pyproject.toml poetry.lock ./
COPY fishing/ ./fishing/
RUN poetry install

# The default port for Cloud Run
EXPOSE 8080

# Main command
CMD ["poetry", "run", "python", "fishing/simulate.py"]
