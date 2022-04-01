"""
Wrappers for gRPC clients.
"""
from abc import ABC

import grpc


class GrpcClient(ABC):
    def __init__(self, addr: str, grpc_stub):
        self.channel = grpc.insecure_channel(addr)
        self.stub = grpc_stub(self.channel)

    def __del__(self):
        self.channel.close()
