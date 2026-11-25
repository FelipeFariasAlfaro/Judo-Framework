"""Deterministic HTTP fixture server used by the regression and feature tests."""
import hashlib
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

USERS = [
    {"id": 1, "name": "Ana", "email": "ana@example.com", "active": True},
    {"id": 2, "name": "Luis", "email": "luis@example.com", "active": False},
]
USER_1 = {
    "id": 1, "name": "Ana", "email": "ana@example.com", "active": True, "nickname": None,
    "uuid": "123e4567-e89b-12d3-a456-426614174000", "website": "https://example.com",
    "created": "2024-01-15T10:30:00Z", "age": 30,
    "address": {"city": "Santiago", "zip": "8320000"}, "tags": ["a", "b"],
}
XML_DOC = ('<?xml version="1.0"?><root xmlns:x="urn:x"><user id="1"><name>Ana</name></user>'
           '<user id="2"><name>Luis</name></user><x:meta>v1</x:meta></root>')


SOAP_OK = ('<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
           '<soap:Body><Result><Code>0</Code><Message>ok</Message></Result></soap:Body></soap:Envelope>')
SOAP_FAULT = ('<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
              '<soap:Body><soap:Fault><faultcode>soap:Server</faultcode><faultstring>Boom happened</faultstring>'
              '</soap:Fault></soap:Body></soap:Envelope>')


class State:
    def __init__(self):
        self.lock = threading.Lock()
        self.counters = {}

    def hit(self, key):
        with self.lock:
            self.counters[key] = self.counters.get(key, 0) + 1
            return self.counters[key]


class Handler(BaseHTTPRequestHandler):
    server_version = "JudoFixture/1.0"

    def log_message(self, *a):
        pass

    def _send(self, status=200, body=None, headers=None, raw=None, ctype="application/json"):
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else b"")
        self.send_response(status)
        if data:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        return self.rfile.read(n) if n else b""

    def _route(self, method):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        path, st = u.path, self.server.state
        body = self._body()

        if path == "/health":
            return self._send(200, {"status": "ok"})
        if path == "/users" and method == "GET":
            return self._send(200, USERS)
        if path == "/users" and method == "POST":
            data = json.loads(body or b"{}")
            data["id"] = 99
            return self._send(201, data)
        if path == "/users/1":
            if method == "GET":
                return self._send(200, USER_1)
            if method in ("PUT", "PATCH"):
                data = json.loads(body or b"{}")
                return self._send(200, {**USER_1, **data})
            if method == "DELETE":
                return self._send(200, {"deleted": True})
        if path == "/echo":
            return self._send(200, {"method": method, "query": q,
                                    "headers": {k.lower(): v for k, v in self.headers.items()},
                                    "body": body.decode("utf-8", "replace")})
        if path == "/slow":
            time.sleep(float(q.get("ms", 0)) / 1000)
            return self._send(200, {"slept": q.get("ms", "0")})
        if path == "/flaky":
            n = st.hit("flaky")
            return self._send(500, {"attempt": n}) if n <= 2 else self._send(200, {"attempt": n})
        if path == "/reset":
            st.counters.clear()
            return self._send(200, {"reset": True})
        if path == "/job":
            n = st.hit("job")
            return self._send(200, {"state": "done" if n >= 3 else "pending", "polls": n})
        if path == "/pages":
            page = int(q.get("page", 1))
            items = [{"id": page * 10 + i} for i in range(3)] if page <= 3 else []
            return self._send(200, {"items": items, "page": page})
        if path == "/xml":
            return self._send(200, raw=XML_DOC.encode(), ctype="application/xml")
        if path == "/secure":
            return self._send(200, {"ok": True}, headers={
                "Strict-Transport-Security": "max-age=31536000", "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY", "Content-Security-Policy": "default-src 'self'"})
        if path == "/download":
            return self._send(200, raw=b"hello judo", ctype="application/octet-stream")
        if path == "/upload" and method == "POST":
            return self._send(200, {"size": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                                    "content_type": self.headers.get("Content-Type", ""),
                                    "has_filename": b'filename="' in body})
        if path == "/form" and method == "POST":
            fields = {k: v[0] for k, v in parse_qs(body.decode()).items()}
            return self._send(200, {"fields": fields, "content_type": self.headers.get("Content-Type", "")})
        if path == "/text":
            return self._send(200, raw=b"hello,world\nsecond line", ctype="text/plain; charset=utf-8")
        if path == "/csv":
            return self._send(200, raw=b"id,name\n1,Ana\n2,Luis\n", ctype="text/csv")
        if path == "/file":
            return self._send(200, raw=b"report-data", ctype="application/octet-stream",
                              headers={"Content-Disposition": 'attachment; filename="report.txt"'})
        if path == "/soap" and method == "POST":
            text = body.decode()
            if "FAULT" in text:
                return self._send(500, raw=SOAP_FAULT.encode(), ctype="text/xml")
            return self._send(200, raw=SOAP_OK.encode(), ctype="text/xml", headers={
                "X-Seen-Action": self.headers.get("SOAPAction", ""), "X-Seen-Type": self.headers.get("Content-Type", "").split(";")[0],
                "X-Seen-Params": self.headers.get("Content-Type", "").partition(";")[2].strip().replace('"', "'")})
        if path == "/xml-post" and method == "POST":
            return self._send(200, raw=body, ctype=self.headers.get("Content-Type", "application/xml"))
        if path == "/sse":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            for i in range(1, 4):
                self.wfile.write(f'event: tick\ndata: {{"n": {i}, "msg": "hello {i}"}}\n\n'.encode())
                self.wfile.flush()
                time.sleep(0.05)
            self.wfile.write(b'event: done\ndata: {"n": 4}\n\n')
            self.wfile.flush()
            return
        if path == "/graphql" and method == "POST":
            payload = json.loads(body or b"{}")
            q, v = payload.get("query", ""), payload.get("variables") or {}
            if "__schema" in q:
                return self._send(200, {"data": {"__schema": {"types": [
                    {"name": "Query", "kind": "OBJECT"}, {"name": "User", "kind": "OBJECT"}]}}})
            if "boom" in q:
                return self._send(200, {"errors": [{"message": "Cannot query field boom"}], "data": None})
            if "createUser" in q:
                return self._send(200, {"data": {"createUser": {"id": 7, "name": v.get("name", "?")}}})
            if "users" in q:
                return self._send(200, {"data": {"users": USERS}})
            return self._send(200, {"data": {"hello": v.get("who", "world")}})
        if path == "/status":
            return self._send(int(q.get("code", 200)), {"code": int(q.get("code", 200))})
        return self._send(404, {"error": "not found", "path": path})

    def do_GET(self): self._route("GET")
    def do_POST(self): self._route("POST")
    def do_PUT(self): self._route("PUT")
    def do_PATCH(self): self._route("PATCH")
    def do_DELETE(self): self._route("DELETE")


class FixtureServer:
    def __init__(self, port=0):
        self.httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.httpd.state = State()
        self.port = self.httpd.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}"
        self._t = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def start(self):
        self._t.start()
        return self

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
