"""
gRPC Assistant client.
"""
from services.assistant.assistant_pb2_grpc import AssistantStub
from utils.grpc.client import GrpcClient


class AssistantGrpcClient(GrpcClient):
    def __init__(self, addr: str):
        super().__init__(addr, AssistantStub)
