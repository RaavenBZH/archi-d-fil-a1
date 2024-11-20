# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import showtime_pb2 as showtime__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in showtime_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ShowtimeStub(object):
    """Définition du service Showtime
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Home = channel.unary_unary(
                '/Showtime/Home',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=showtime__pb2.ShowtimeHomeResponse.FromString,
                _registered_method=True)
        self.GetAllSchedules = channel.unary_stream(
                '/Showtime/GetAllSchedules',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=showtime__pb2.Schedule.FromString,
                _registered_method=True)
        self.GetSchedule = channel.unary_unary(
                '/Showtime/GetSchedule',
                request_serializer=showtime__pb2.Date.SerializeToString,
                response_deserializer=showtime__pb2.Schedule.FromString,
                _registered_method=True)
        self.AddSchedule = channel.unary_unary(
                '/Showtime/AddSchedule',
                request_serializer=showtime__pb2.Schedule.SerializeToString,
                response_deserializer=showtime__pb2.Schedule.FromString,
                _registered_method=True)


class ShowtimeServicer(object):
    """Définition du service Showtime
    """

    def Home(self, request, context):
        """Endpoint pour la page d'accueil
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllSchedules(self, request, context):
        """Endpoint pour récupérer la base de données complète
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSchedule(self, request, context):
        """Endpoint pour récupérer le programme par date
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddSchedule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ShowtimeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Home': grpc.unary_unary_rpc_method_handler(
                    servicer.Home,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=showtime__pb2.ShowtimeHomeResponse.SerializeToString,
            ),
            'GetAllSchedules': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAllSchedules,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=showtime__pb2.Schedule.SerializeToString,
            ),
            'GetSchedule': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSchedule,
                    request_deserializer=showtime__pb2.Date.FromString,
                    response_serializer=showtime__pb2.Schedule.SerializeToString,
            ),
            'AddSchedule': grpc.unary_unary_rpc_method_handler(
                    servicer.AddSchedule,
                    request_deserializer=showtime__pb2.Schedule.FromString,
                    response_serializer=showtime__pb2.Schedule.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Showtime', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Showtime', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Showtime(object):
    """Définition du service Showtime
    """

    @staticmethod
    def Home(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Showtime/Home',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            showtime__pb2.ShowtimeHomeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllSchedules(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/Showtime/GetAllSchedules',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            showtime__pb2.Schedule.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSchedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Showtime/GetSchedule',
            showtime__pb2.Date.SerializeToString,
            showtime__pb2.Schedule.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddSchedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Showtime/AddSchedule',
            showtime__pb2.Schedule.SerializeToString,
            showtime__pb2.Schedule.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
