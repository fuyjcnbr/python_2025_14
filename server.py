import os
import psutil
import socket
from dataclasses import dataclass
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor


RESP_GET = b"""HTTP/1.1 200 OK\r
Content-Length: 63\r
Content-Type: text/html\r
Connection: Closed\r
\r
<html>\r\n
<body>\r\n
<h1>Hello, World!</h1>\r\n
</body>\r\n
</html>\r\n
"""


RESP_HEAD = b"""HTTP/1.1 200 OK\r
\r
"""


RESP_WRONG_PAGE = b"""HTTP/1.1 200 OK\r
Content-Length: 63\r
Content-Type: text/html\r
Connection: Closed\r
\r
<html>\r\n
<body>\r\n
<h1>Wrong page or method!</h1>\r\n
</body>\r\n
</html>\r\n
"""


@dataclass
class HttpRequest:
    method: str
    path: str


class MyHTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        print(f"cpu_count()={cpu_count()}")
        self.process_executor = ProcessPoolExecutor(cpu_count() - 1)

    def serve_forever(self):
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0,
        )
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            while True:
                conn, _ = serv_sock.accept()
                try:
                    future = self.process_executor.submit(MyHTTPServer.serve_client, conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    @staticmethod
    def serve_client(conn):
        core_id = psutil.Process().cpu_num()
        print(f"serve_client new client pid={os.getpid()}, core_id={core_id}")
        try:
            req = MyHTTPServer.parse_request(conn)
            resp = MyHTTPServer.handle_request(req)
            MyHTTPServer.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            print(e)

        if conn:
            conn.close()

    @staticmethod
    def parse_request(conn) -> HttpRequest:
        data = conn.recv(1024)
        li = data.decode().strip().split(" ")
        req = HttpRequest(method=li[0], path=li[1])
        return req

    @staticmethod
    def handle_request(req):
        if req.path == "/test" and req.method == "GET":
          return MyHTTPServer.handle_get()
        elif req.path == "/test" and req.method == "HEAD":
          return MyHTTPServer.handle_head()
        else:
            return MyHTTPServer.handle_wrong_page()

    @staticmethod
    def send_response(conn, resp):
        conn.send(resp)

    @staticmethod
    def handle_get():
        resp = RESP_GET
        return resp

    @staticmethod
    def handle_head():
        resp = RESP_HEAD
        return resp

    @staticmethod
    def handle_wrong_page():
        resp = RESP_WRONG_PAGE
        return resp


serv = MyHTTPServer(host="0.0.0.0", port=80)

try:
    serv.serve_forever()
except KeyboardInterrupt:
    pass
