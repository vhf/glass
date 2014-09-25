from router import route


@route('\A\Z')
def hello_world(args):
  return 'hello world'


@route('\Ahello/(\w+)\Z')
def hello(to):
  return 'hello {}'.format(to.group(1))
