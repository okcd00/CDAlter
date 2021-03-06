# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import keyvaluestore_pb2 as keyvaluestore__pb2


class KeyValueStoreStub(object):
    """A simple key-value storage service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ask = channel.unary_unary(
                '/keyvaluestore.KeyValueStore/ask',
                request_serializer=keyvaluestore__pb2.Key.SerializeToString,
                response_deserializer=keyvaluestore__pb2.Response.FromString,
                )
        self.remember = channel.unary_unary(
                '/keyvaluestore.KeyValueStore/remember',
                request_serializer=keyvaluestore__pb2.Item.SerializeToString,
                response_deserializer=keyvaluestore__pb2.Response.FromString,
                )


class KeyValueStoreServicer(object):
    """A simple key-value storage service
    """

    def ask(self, request, context):
        """Provides a value for each key request
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remember(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeyValueStoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ask': grpc.unary_unary_rpc_method_handler(
                    servicer.ask,
                    request_deserializer=keyvaluestore__pb2.Key.FromString,
                    response_serializer=keyvaluestore__pb2.Response.SerializeToString,
            ),
            'remember': grpc.unary_unary_rpc_method_handler(
                    servicer.remember,
                    request_deserializer=keyvaluestore__pb2.Item.FromString,
                    response_serializer=keyvaluestore__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'keyvaluestore.KeyValueStore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KeyValueStore(object):
    """A simple key-value storage service
    """

    @staticmethod
    def ask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/keyvaluestore.KeyValueStore/ask',
            keyvaluestore__pb2.Key.SerializeToString,
            keyvaluestore__pb2.Response.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def remember(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/keyvaluestore.KeyValueStore/remember',
            keyvaluestore__pb2.Item.SerializeToString,
            keyvaluestore__pb2.Response.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
