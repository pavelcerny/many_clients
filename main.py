#!/usr/bin/python3
__author__ = 'Pavel'

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

words = {}

class OSPHTTPHandler(BaseHTTPRequestHandler,threading.Thread):
    def do_POST(self):
        global words
        if self.path == "/osp/myserver/data":
            length = int(self.headers.get('Content-Length'))
            text = self.rfile.read(length).decode("utf-8")
            for word in text.split():
                words[word] = 1;
            self.send_response(204) # No Content
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        global words
        if self.path == "/osp/myserver/count":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(len(words)).encode())
            words = {}
        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer(('', 8000), OSPHTTPHandler)
print("Listening on port", httpd.server_port)
httpd.serve_forever()