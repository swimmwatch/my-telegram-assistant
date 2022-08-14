FROM python:3.10

WORKDIR /app

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

COPY poetry.lock .
COPY pyproject.toml .

# Install Python dependecies
RUN poetry install --no-dev

# Build gRPC services
COPY protobufs /app/protobufs
RUN poetry run python -m grpc_tools.protoc \
    -I /app/protobufs \
    --python_out=. \
     --grpc_python_out=. \
    /app/protobufs/services/**/**.proto

COPY . .