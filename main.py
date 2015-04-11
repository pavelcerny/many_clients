#!/usr/bin/python3
__author__ = 'Pavel'

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

threadCounter = 0
postThreads = []
getT = None

words = {}
getIsWaiting = 0
getIsRunning = threading.Lock()


class postThread (threading.Thread):
    def __init__(self, request):
        threading.Thread.__init__(self)
    def run(self):
        print ("post")
        # global words
        # if self.request.path == "/osp/myserver/data":
        #     length = int(self.request.headers.get('Content-Length'))
        #     text = self.request.rfile.read(length).decode("utf-8")
        #     for word in text.split():
        #         words[word] = 1
        #     self.request.send_response(204) # No Content
        #     self.request.end_headers()
        # else:
        #     self.request.send_response(404)
        #     self.request.end_headers()


class getThread (threading.Thread):
    def __init__(self, request):
        threading.Thread.__init__(self)
    def run(self):
        print ("get")
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




class OSPHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global postThreads
        t = postThread(self)
        postThreads.append(t)
        t.start()


    def do_GET(self):
        global postThreads, getT
        getT = getThread(self)
        for t in postThreads:
            t.join()
        postThreads=[]
        getT.run()
        getT=None

httpd = HTTPServer(('', 8000), OSPHTTPHandler)
print("Listening on port", httpd.server_port)
#httpd.serve_forever()

#process post requests simultaneously, but wait when get request
while 1:
    if getT is None:
        httpd.handle_request()
    else:
        getT.join()