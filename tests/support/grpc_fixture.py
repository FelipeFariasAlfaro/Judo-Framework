"""In-process gRPC server with reflection, built from a dynamically created protobuf descriptor."""
import time
from concurrent import futures

import grpc
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from grpc_reflection.v1alpha import reflection

PACKAGE = "judo.test"
SERVICE = f"{PACKAGE}.Greeter"


def _build():
    pool = descriptor_pool.Default()
    try:
        pool.FindFileByName("judo_greeter.proto")
    except KeyError:
        fdp = descriptor_pb2.FileDescriptorProto(name="judo_greeter.proto", package=PACKAGE, syntax="proto3")
        F = descriptor_pb2.FieldDescriptorProto
        req = fdp.message_type.add(name="HelloRequest")
        req.field.add(name="name", number=1, type=F.TYPE_STRING, label=F.LABEL_OPTIONAL)
        req.field.add(name="times", number=2, type=F.TYPE_INT32, label=F.LABEL_OPTIONAL)
        rep = fdp.message_type.add(name="HelloReply")
        rep.field.add(name="message", number=1, type=F.TYPE_STRING, label=F.LABEL_OPTIONAL)
        rep.field.add(name="count", number=2, type=F.TYPE_INT32, label=F.LABEL_OPTIONAL)
        svc = fdp.service.add(name="Greeter")
        svc.method.add(name="SayHello", input_type=f".{PACKAGE}.HelloRequest", output_type=f".{PACKAGE}.HelloReply")
        svc.method.add(name="Countdown", input_type=f".{PACKAGE}.HelloRequest", output_type=f".{PACKAGE}.HelloReply",
                       server_streaming=True)
        pool.Add(fdp)
    req_cls = message_factory.GetMessageClass(pool.FindMessageTypeByName(f"{PACKAGE}.HelloRequest"))
    rep_cls = message_factory.GetMessageClass(pool.FindMessageTypeByName(f"{PACKAGE}.HelloReply"))
    return req_cls, rep_cls


class GrpcFixture:
    def __init__(self):
        Req, Rep = _build()

        def say_hello(request, context):
            md = dict(context.invocation_metadata())
            if request.name == "missing":
                context.abort(grpc.StatusCode.NOT_FOUND, "nobody home")
            if request.name == "secure" and md.get("authorization") != "Bearer ok":
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "token required")
            if request.name == "slow":
                time.sleep(0.2)
            return Rep(message=f"Hello {request.name}", count=len(request.name))

        def countdown(request, context):
            for i in range(request.times, 0, -1):
                yield Rep(message=f"T-{i}", count=i)

        handlers = {
            "SayHello": grpc.unary_unary_rpc_method_handler(
                say_hello, request_deserializer=Req.FromString, response_serializer=Rep.SerializeToString),
            "Countdown": grpc.unary_stream_rpc_method_handler(
                countdown, request_deserializer=Req.FromString, response_serializer=Rep.SerializeToString),
        }
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        self.server.add_generic_rpc_handlers((grpc.method_handlers_generic_handler(SERVICE, handlers),))
        reflection.enable_server_reflection((SERVICE, reflection.SERVICE_NAME), self.server)
        self.port = self.server.add_insecure_port("127.0.0.1:0")
        self.target = f"127.0.0.1:{self.port}"

    def start(self):
        self.server.start()
        return self

    def stop(self):
        self.server.stop(0)
