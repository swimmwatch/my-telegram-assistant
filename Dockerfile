FROM python:3.9

WORKDIR /app

# Install dependencies for TDLib
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libssl-dev \
    libc++-dev \
    libc++abi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

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