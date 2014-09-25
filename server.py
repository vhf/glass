import BaseHTTPServer
import os
import time
import argparse
import re
import cgi
from router import Router, ROUTES
import routes

HOST_NAME = 'localhost'
PORT_NUM = 4242


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = Router(self)
        for key, value in ROUTES.items():
            self.router.add(key, value)
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/'):
            self.path = self.path[1:]

        routing_info = self.router.route(self.path)
        if routing_info:
            func, regex_match = routing_info
            content = func(regex_match)

            self.do_HEAD()
            self.wfile.write(content)
            return

        self.send_error(404)

    def do_POST(self):
        form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={'REQUEST_METHOD':'POST',
                                         'CONTENT_TYPE':self.headers['Content-Type'],
                                         })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
                field_item = form[field]
                if field_item.filename:
                        # The field contains an uploaded file
                        file_data = field_item.file.read()
                        file_len = len(file_data)
                        del file_data
                        self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                                        (field, field_item.filename, file_len))
                else:
                        # Regular form value
                        self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        return

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUM), Handler)
    print '<Ctrl-c> to exit'
    print time.asctime(), 'Server starts - {}:{}'.format(HOST_NAME, PORT_NUM)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
