"""
Dynamic gRPC client driven by server reflection (no .proto files needed).

Requires the optional extra: ``pip install "judo-framework[grpc]"``
(grpcio, grpcio-reflection, protobuf). Supports unary and server-streaming calls with
JSON-encoded requests/responses.
"""
import time
from typing import Any, Dict, List, Optional, Tuple

_INSTALL = "gRPC steps need extra packages: pip install 'judo-framework[grpc]'"


def _deps():
    try:
        import grpc
        from google.protobuf import descriptor_pool, json_format, message_factory
        from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
    except ImportError as exc:
        raise AssertionError(f"{_INSTALL} ({exc})")
    return grpc, descriptor_pool, json_format, message_factory, reflection_pb2, reflection_pb2_grpc


def normalize_method(method: str) -> Tuple[str, str]:
    """'pkg.Service/Method' or 'pkg.Service.Method' -> ('pkg.Service', 'Method')."""
    method = method.strip().lstrip("/")
    if "/" in method:
        service, name = method.split("/", 1)
    else:
        service, _, name = method.rpartition(".")
    assert service and name, f"Invalid gRPC method '{method}'. Use 'package.Service/Method'"
    return service, name


def _message_class(message_factory, descriptor):
    if hasattr(message_factory, "GetMessageClass"):
        return message_factory.GetMessageClass(descriptor)
    return message_factory.MessageFactory().GetPrototype(descriptor)  # pragma: no cover


def _to_dict(json_format, message) -> Dict[str, Any]:
    try:
        return json_format.MessageToDict(message, preserving_proto_field_name=True,
                                         always_print_fields_with_no_presence=True)
    except TypeError:  # older protobuf
        return json_format.MessageToDict(message, preserving_proto_field_name=True,
                                         including_default_value_fields=True)


class GrpcClient:
    def __init__(self, target: str, tls: bool = False, timeout: float = 10.0):
        self.grpc, self._pool_mod, self._json, self._factory, self._rpb, self._rpb_grpc = _deps()
        self.target = target
        self.timeout = timeout
        self.metadata: List[Tuple[str, str]] = []
        self.channel = (self.grpc.secure_channel(target, self.grpc.ssl_channel_credentials())
                        if tls else self.grpc.insecure_channel(target))
        self._pools: Dict[str, Any] = {}
        self.last_status = "OK"
        self.last_details = ""
        self.last_elapsed_ms = 0.0

    # -- reflection ---------------------------------------------------------
    def _reflect(self, **request):
        stub = self._rpb_grpc.ServerReflectionStub(self.channel)
        req = self._rpb.ServerReflectionRequest(**request)
        try:
            return list(stub.ServerReflectionInfo(iter([req]), timeout=self.timeout))
        except self.grpc.RpcError as exc:
            raise AssertionError(f"gRPC reflection failed on {self.target}: {exc.code().name} {exc.details()}")

    def list_services(self) -> List[str]:
        responses = self._reflect(list_services="*")
        return [s.name for r in responses for s in r.list_services_response.service]

    def _pool_for(self, service: str):
        if service in self._pools:
            return self._pools[service]
        responses = self._reflect(file_containing_symbol=service)
        blobs = [b for r in responses for b in r.file_descriptor_response.file_descriptor_proto]
        assert blobs, f"The server does not know the service '{service}'. Available: {self.list_services()}"
        pool = self._pool_mod.DescriptorPool()
        pending = list(blobs)
        for _ in range(len(pending) + 1):
            still = []
            for blob in pending:
                try:
                    pool.AddSerializedFile(blob)
                except Exception:  # dependency not loaded yet
                    still.append(blob)
            pending = still
            if not pending:
                break
        assert not pending, "Could not load the service descriptors (missing dependencies)"
        self._pools[service] = pool
        return pool

    def method_descriptor(self, method: str):
        service, name = normalize_method(method)
        pool = self._pool_for(service)
        try:
            return pool, pool.FindServiceByName(service).FindMethodByName(name)
        except KeyError:
            methods = [m.name for m in pool.FindServiceByName(service).methods]
            raise AssertionError(f"Method '{name}' not found in {service}. Available: {methods}")

    def has_method(self, method: str) -> bool:
        try:
            self.method_descriptor(method)
            return True
        except AssertionError:
            return False

    # -- calls --------------------------------------------------------------
    def _prepare(self, method: str, request_json: str):
        service, name = normalize_method(method)
        _, desc = self.method_descriptor(method)
        req_cls = _message_class(self._factory, desc.input_type)
        resp_cls = _message_class(self._factory, desc.output_type)
        try:
            request = self._json.Parse(request_json or "{}", req_cls())
        except self._json.ParseError as exc:
            raise AssertionError(f"Request does not match {desc.input_type.full_name}: {exc}")
        return f"/{service}/{name}", desc, request, resp_cls

    def _record(self, code, details, started):
        self.last_status = code.name
        self.last_details = details or ""
        self.last_elapsed_ms = round((time.time() - started) * 1000, 2)

    def call(self, method: str, request_json: str) -> Optional[Dict[str, Any]]:
        path, desc, request, resp_cls = self._prepare(method, request_json)
        assert not desc.client_streaming, "Client-streaming calls are not supported"
        started = time.time()
        if desc.server_streaming:
            raise AssertionError("This is a server-streaming method: use 'I send the gRPC streaming request'")
        rpc = self.channel.unary_unary(path, request_serializer=request.__class__.SerializeToString,
                                       response_deserializer=resp_cls.FromString)
        try:
            response = rpc(request, timeout=self.timeout, metadata=self.metadata or None)
        except self.grpc.RpcError as exc:
            self._record(exc.code(), exc.details(), started)
            return None
        self._record(self.grpc.StatusCode.OK, "", started)
        return _to_dict(self._json, response)

    def stream(self, method: str, request_json: str) -> List[Dict[str, Any]]:
        path, desc, request, resp_cls = self._prepare(method, request_json)
        assert desc.server_streaming and not desc.client_streaming, \
            "This step needs a server-streaming method"
        started = time.time()
        rpc = self.channel.unary_stream(path, request_serializer=request.__class__.SerializeToString,
                                        response_deserializer=resp_cls.FromString)
        messages = []
        try:
            for msg in rpc(request, timeout=self.timeout, metadata=self.metadata or None):
                messages.append(_to_dict(self._json, msg))
        except self.grpc.RpcError as exc:
            self._record(exc.code(), exc.details(), started)
            return messages
        self._record(self.grpc.StatusCode.OK, "", started)
        return messages

    def close(self):
        self.channel.close()
