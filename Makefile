build-protobuf:
	poetry run python -m grpc_tools.protoc \
    -I protobufs \
    --python_out=. \
    --grpc_python_out=. \
    protobufs/services/**/**.proto
