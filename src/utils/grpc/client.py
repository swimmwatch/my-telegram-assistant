"""
Wrappers for gRPC clients.
"""
import abc

import grpc


class GrpcClient(abc.ABC):
    def __init__(self, addr: str, grpc_stub):
        self.channel = grpc.insecure_channel(addr)
        self.stub = grpc_stub(self.channel)

    def __del__(self):
        self.channel.close()
