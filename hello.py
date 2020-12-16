from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.write('<h3>hello,tornado</h3>')

if __name__ == '__main__':
    app = Application([
        ('/',IndexHandler)
    ])
    app.listen(7000)
    print('starting http://localhost:%s' % 7000)
    IOLoop.current().start()