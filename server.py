import BaseHTTPServer
import os
import time

HOST_NAME = 'localhost'
PORT_NUM = 4242


def hello_world():
  return 'hello world'

def bar():
  return 'bar'


routes = {
  '/': hello_world,
  '/index': hello_world,
  '/bar': bar
}

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self.file_path = os.getcwd() + '/index.html'
    self.do_HEAD()
    self.wfile.write(routes[self.path]())

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
