FROM python:3.9

WORKDIR /app

COPY . .

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

# Install Python dependecies
RUN poetry install --no-dev

# Install playwright
RUN poetry run playwright install
RUN poetry run playwright install-deps

# Build gRPC services
RUN poetry run python -m grpc_tools.protoc \
    -I /app/protobufs \
    --python_out=. \
     --grpc_python_out=. \
    /app/protobufs/services/assistant/assistant.proto
