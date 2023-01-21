build-protobuf:
	poetry run python -m grpc_tools.protoc \
    -I src/protobufs \
    --python_out=src \
    --grpc_python_out=src \
    src/protobufs/services/*/*.proto
