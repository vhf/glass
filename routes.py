from router import route


@route('\A\Z')
def hello_world():
    return 'hello world'


@route('\Ahello/(?P<name>\w+)\Z')
def hello(name):
    return 'hello {}'.format(name)
