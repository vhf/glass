import re

ROUTES = {}


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


def route(route):
    def wrap(f):
        ROUTES[route] = f
    return wrap
