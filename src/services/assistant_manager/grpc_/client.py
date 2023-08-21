"""
Assistant manager gPRC client.
"""
from services.assistant_manager.assistant_manager_pb2_grpc import AssistantManagerStub
from utils.grpc.client import AsyncGrpcClient
from utils.grpc.client import GrpcClient


class AssistantManagerGrpcClient(GrpcClient):
    class Meta:
        stub = AssistantManagerStub


class AssistantManagerAsyncGrpcClient(AsyncGrpcClient):
    class Meta:
        stub = AssistantManagerStub
