SRC_DIR=src

build-protobuf:
	poetry run python -m grpc_tools.protoc \
    -I src/protobufs \
    --python_out=$(SRC_DIR) \
    --grpc_python_out=$(SRC_DIR) \
    --mypy_out=$(SRC_DIR) \
    $(SRC_DIR)/protobufs/services/*/*.proto

mypy:
	poetry run mypy $(SRC_DIR)

flake:
	poetry run flake8 $(SRC_DIR)

lint: flake mypy

unit-test:
	poetry run pytest $(SRC_DIR)

cov:
	poetry run pytest --cov=$(SRC_DIR) $(SRC_DIR)

black:
	poetry run black $(SRC_DIR)
