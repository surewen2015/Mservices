import json
import uuid

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import options,define,parse_command_line

class loginHandler(RequestHandler):

    users = [{
        'id': 1,
        'name': 'zhoujielun',
        'pwd': '123',
        'last_login_device': 'Android 5.1 Oneplus5'
    }]

    def get(self):
        bytes = self.request.body
        print(bytes)
        print(self.request.headers.get('Content-Type'))

        content_type = self.request.headers.get('Content-Type')
        if content_type.startswith('application/json'):
            #self.write('upload json ok')
            json_str = bytes.decode('utf-8')
            json_data = json.loads(json_str)
            resp_data={}
            login_user = None
            for user in self.users:
                if user['name'] == json_data['name']:
                    if user['pwd'] == json_data['pwd']:
                        login_user = user
                        break

            if login_user:
                resp_data['msg'] = 'success'
                resp_data['token'] = uuid.uuid4().hex
            else:
                resp_data['msg'] = '查无此用户'
            self.write(resp_data)
            self.set_header('Content-Type', 'application/json')
        else:
            self.write('upload data 必须是json格式')








        #self.write('<h3>get login</h3>')

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass



def make_app():
    return Application(
        handlers=[
            ('/user', loginHandler),
        ],
        default_host=options.h)

if __name__ == '__main__':

    define('p', default=8000, type=int, help='绑定的port端口')
    define('h', default='localhost', type=str, help='绑定的主机ip')

    parse_command_line()

    app = make_app()
    app.listen(options.p)
    print('running server...%s:%s'% (options.h, options.p))
    IOLoop.current().start()