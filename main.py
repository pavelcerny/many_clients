#!/usr/bin/python3
__author__ = 'Pavel'

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading


postThreads = []
getT = None

words = {}
threadLock = threading.Lock()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class PostThread (threading.Thread):
    def __init__(self, request):
        threading.Thread.__init__(self)
        self.request = request
    def run(self):
        print ("post-thread", self.request.path)
        global words
        if self.request.path == "/osp/myserver/data":
            length = int(self.request.headers.get('Content-Length'))
            text = self.request.rfile.read(length).decode("utf-8")
            for word in text.split():
                words[word] = 1
            self.request.send_response(204) # No Content
            self.request.end_headers()
        else:
            self.request.send_response(404)
            self.request.end_headers()


class GetThread (threading.Thread):
    def __init__(self, request):
        threading.Thread.__init__(self)
        self.request = request
    def run(self):
        print ("get-thread", self.request.path)
        # global words
        # if self.request.path == "/osp/myserver/count":
        #     self.request.send_response(200)
        #     self.request.send_header("Content-type", "text/plain")
        #     self.request.end_headers()
        #     self.request.wfile.write(str(len(words)).encode())
        #     words = {}
        # else:
        #     self.request.send_response(404)
        #     self.request.end_headers()




class ThreadedOSPHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("post")
        global postThreads
        t = threading.current_thread()
        postThreads.append(t)
        #do the handling now
        global words
        if self.path == "/osp/myserver/data":
            length = int(self.headers.get('Content-Length'))
            text = self.rfile.read(length).decode("utf-8")
            for word in text.split():
                words[word] = 1
            self.send_response(204) # No Content
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        print ("get")
        global postThreads, getT
        getT = threading.current_thread()
        for t in postThreads:
            t.join()
        postThreads=[]
        #do the handling now
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
        # end of handling
        getT=None

httpd = ThreadedHTTPServer(('', 8000), ThreadedOSPHTTPHandler)
print("Listening on port", httpd.server_port)
#httpd.serve_forever()

#process post requests simultaneously, but wait when get request
while 1:
    if getT is None:
        print("handling request")
        httpd.handle_request()
    else:
        getT.join()