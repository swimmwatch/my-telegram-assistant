ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim-buster as build

ENV POETRY_VERSION=1.3.2

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc curl

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# Copy installed packages
COPY --from=build /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application
COPY src .

# Build gRPC services
RUN python -m grpc_tools.protoc \
    -I protobufs \
    --python_out=. \
    --grpc_python_out=. \
    protobufs/services/**/**.proto
