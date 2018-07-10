# execute in the folder you want the server to run
# starts at port 80

import os
from urllib import parse
import http.server
import socketserver

HOST = ('0.0.0.0', 80)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parts = parse.urlparse(self.path)
        request_file_path = url_parts.path.strip("/")
        if not os.path.exists(request_file_path):
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)



httpd = socketserver.TCPServer(HOST, Handler)
httpd.serve_forever()
