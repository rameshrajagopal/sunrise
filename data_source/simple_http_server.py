#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer

import sys
import os

class HttpServer(object):
    def __init__(self, port, data_source_path):
        self.port = port
        self.path = data_source_path
        self.handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    def start(self):
        os.chdir(self.path)
        print "Starting http server on ", self.port
        httpd = SocketServer.TCPServer(("", self.port), self.handler)
        httpd.serve_forever()

#main
if __name__ == "__main__":
    if len(sys.argv) != 3:
       print "Usage is wrong"
       print sys.argv[0] + " port data_source_path" 
       sys.exit(-1)
    data_producer = HttpServer(int(sys.argv[1]), sys.argv[2])
    data_producer.start()


