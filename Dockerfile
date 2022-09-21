FROM python:3.10

WORKDIR /app

# Install Python dependecies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Build gRPC services
COPY protobufs /app/protobufs
RUN python -m grpc_tools.protoc \
    -I /app/protobufs \
    --python_out=. \
     --grpc_python_out=. \
    /app/protobufs/services/**/**.proto

COPY . .