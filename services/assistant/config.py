"""
Telegram assistant configuration.
"""

import os

# TDLib
AIOTDLIB_API_ID = int(os.environ.get('AIOTDLIB_API_ID', 0))
AIOTDLIB_API_HASH = os.environ.get('AIOTDLIB_API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')

# gRPC server
ASSISTANT_GRPC_PORT = os.environ.get('ASSISTANT_GRPC_PORT')
ASSISTANT_GRPC_HOST = os.environ.get('ASSISTANT_GRPC_HOST')
