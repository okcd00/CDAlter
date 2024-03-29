# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : grpc_client.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-04-16
#   desc     : client in grpc service
# ==========================================================================
import os
import sys
if os.environ.get('https_proxy'):
    del os.environ['https_proxy']
if os.environ.get('http_proxy'):
    del os.environ['http_proxy']
import grpc

"""
# generate it at first
python -m grpc_tools.protoc \
    -I ./ \ 
    --python_out=. \
    --grpc_python_out=. \
    keyvaluestore.proto
# then you can get keyvaluestore_pb2_grpc and keyvaluestore_pb2
"""
sys.path.append('./protos/')
from interactive.protos import keyvaluestore_pb2_grpc, keyvaluestore_pb2


if __name__ == '__main__':
    queries = {'name': 'chendian', 'age': '26', 'gender': 'male'}

    with grpc.insecure_channel('localhost:20416') as channel:
        stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)

        response = stub.remember(keyvaluestore_pb2.Item(key='name', value='cd'))
        print(response)
        response = stub.ask(keyvaluestore_pb2.Key(key='name'))
        print(response)

