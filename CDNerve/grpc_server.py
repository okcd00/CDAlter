# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : grpc_server.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-04-16
#   desc     : server in grpc service
# ==========================================================================
import sys
import time
import grpc
from concurrent import futures
from multiprocessing import Pool
from collections import OrderedDict
from grpc._cython.cygrpc import CompressionAlgorithm, CompressionLevel

"""
# generate it at first
python -m grpc_tools.protoc \
    -I ./ \ 
    --python_out=. \
    --grpc_python_out=. \
    keyvaluestore.proto
# then you can get keyvaluestore_pb2_grpc and keyvaluestore_pb2
"""
sys.path.append('../CDMemory/protos/')
from CDMemory.protos import keyvaluestore_pb2_grpc, keyvaluestore_pb2


class KVServicer(keyvaluestore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.records = OrderedDict()

    def ask(self, request, context):
        _value = self.records.get(request.key, "Empty")
        return keyvaluestore_pb2.Response(value=_value)

    def remember(self, request, context):
        key, value = request.key, request.value
        self.records.update({key: value})
        return keyvaluestore_pb2.Response(
            value="Remembered: the value for {} is {}".format(key, value))


def serve(n_worker=4, port=20416):
    max_receive_message_length = 512
    service = KVServicer()
    service.process_pool = Pool(processes=n_worker)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=n_worker), options=[
        ('grpc.max_receive_message_length', max_receive_message_length),
        ('grpc.default_compression_algorithm', CompressionAlgorithm.gzip),
        ('grpc.grpc.default_compression_level', CompressionLevel.high)
    ])
    keyvaluestore_pb2_grpc.add_KeyValueStoreServicer_to_server(service, server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    # server.wait_for_termination()
    return server


if __name__ == "__main__":
    print("starting server...")
    server_agent = serve()
    print("server started.")
    while True:
        time.sleep(100000)
        print("[ALIVE] {}".format(time.ctime()))
