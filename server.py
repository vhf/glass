import BaseHTTPServer
import os
import time
import argparse
import re
from routes import hello, hello_world


HOST_NAME = 'localhost'
PORT_NUM = 4242

ROUTES = {
  '\Ahello/(\w+)\Z': ('routes', hello),
  '\A\Z': ('routes', hello_world)

}


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
      func_info, regex_match = routing_info
      module_name, func = func_info
      content = func(regex_match)

      self.do_HEAD()
      self.wfile.write(content)
      return

    self.send_error(404)




class Router(object):
  def __init__(self, server):
    self.routes = {}
    self.server = server

  def add(self, route, value):
    self.routes[route] = value

  def route(self, route):
    for pattern in self.routes:
      match = re.match(pattern, route)
      if match:
        return self.routes[pattern], match


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
