import re
from bottle import route, run, response
from datetime import datetime


USER_RE = re.compile('user[\d]+')


@route('/time')
def time():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return datetime.now().strftime("%B %d, %Y %H:%M")


@route('/user/<name>')
def user(name):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return str(USER_RE.match(name) is not None)


run(host='localhost', port=8080, debug=True)
