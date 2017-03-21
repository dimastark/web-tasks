from bottle import route, run, error, request, response
import sqlite3

# Это домашка. Да. Все правильно. В вебе не только фронт

PAGES = ['/', 'hello', '404']


class CounterAPI:
    def __init__(self, memory=False):
        self.conn = sqlite3.connect(':memory:' if memory else 'counters.db')
        with self.conn as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS counters (ip text, page text)')

    def put_current_client(self, visited_page):
        with self.conn as conn:
            conn.execute(
                'INSERT INTO COUNTERS(ip, page) VALUES (?, ?)',
                (request.environ.get('REMOTE_ADDR'), visited_page)
            )

API = CounterAPI()


@route('/')
def index():
    API.put_current_client('/')
    name = 'Anonymous'
    if request.cookies.get('name'):
        name = request.cookies.get('name')
    return '<b>Hello {}</b>'.format(name)


@route('/counts')
def counts():
    API.put_current_client('counts')
    values = {}
    with API.conn as conn:
        cur = conn.execute('SELECT * FROM COUNTERS')
        data = cur.fetchall()
        for ip, page in data:
            key = (ip, page)
            values[key] = values[key] + 1 if key in values else 1
    template = '<table>'
    for visits in values:
        template += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            visits[0], visits[1], values[visits]
        )
    return template + '</table>'


@route('/hello/<name>')
def save_name(name):
    API.put_current_client('hello')
    response.set_cookie('name', name, path='/')
    return 'OK'


@error(404)
def err404(err):
    API.put_current_client('404')
    return '{}, just for you'.format(err)


run(host='localhost', port=8080, debug=True)
