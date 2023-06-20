"""
Assistant manager gPRC client.
"""
from services.assistant_manager.assistant_manager_pb2_grpc import AssistantManagerStub
from utils.grpc.client import GrpcClient


class AssistantManagerGrpcClient(GrpcClient):
    def __init__(self, addr: str):
        super().__init__(addr, AssistantManagerStub)
