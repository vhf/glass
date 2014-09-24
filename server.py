import BaseHTTPServer
import os
import time
import re


HOST_NAME = 'localhost'
PORT_NUM = 4242


def hello_world():
  return 'hello world'

def bar():
  return 'bar'


def hello(to):
  return 'hello {}'.format(to)



routes = {
  '/': hello_world,
  '/index': hello_world,
  '/hello/:to': hello,
  '/bar': bar
}

pattern = re.compile('(?:\:)(\w+)+')


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self.file_path = os.getcwd() + '/index.html'
    self.do_HEAD()

    path_args = pattern.findall(self.path)

    self.wfile.write(path_args)

    if self.path in routes:
      self.wfile.write(routes[self.path]())
    else:
      self.send_error(404)


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
