import json

import tornado.web
import tornado.ioloop
import tornado.options

class IndexHandler(tornado.web.RequestHandler):

    def get(self):

        self.write('<h3>我是主页</h3>')

    def post(self):

        #name = self.get_argument('name')
        #city = self.get_argument('city')
        name = self.get_body_argument('name')
        city = self.get_body_argument('city')

        self.write('<h3>我是post请求方法:%s %s</h3>'%(name, city))

    def put(self):
        self.write('<h3>我是put请求方法</h3>')

    def delete(self):
        self.write('<h3>我是delete请求方法</h3>')

class SearchHandler(tornado.web.RequestHandler):
    mapper = {
        'python': 'ai开发',
        'java': '20年了',
        'H5': '2014开始流行的web语言'
    }
    def get(self):
        html = """
            <h3>搜索%s结果</h3>        
            <p>
                %s
            </p>
        """


        wd = self.get_query_argument('wd')
        result = self.mapper.get(wd)
        #self.write(html % (wd, result))
        resp_data = {
            'wd': wd,
            'result': result
        }
        self.write(json.dumps(resp_data))
        self.set_status(200)
        self.set_header('Content-Type','application/json;charset=utf-8')
        self.set_cookie('wd', wd)

class CookieHandler(tornado.web.RequestHandler):
    def get(self):
        if self.request.arguments.get('name'):

            name = self.get_query_argument('name')

            value = self.get_cookie(name)
            self.write(value)
        else:
            cookies: dict = self.request.cookies
            html = '<ul>%s</ul>'
            lis = []
            for key, value in cookies.items():
                lis.append('<li>%s: %s</li>'% (key, value))
            self.write('显示所有cookie'+html % ' '.join(lis))

    def delete(self):
        name = self.get_argument('name')
        if self.request.cookies.get(name, None):
            self.clear(name)
            self.write('删除%s 成功' % name)
        else:
            self.write('删除%s 失败，不存在' % name)

class OrderHandler(tornado.web.RequestHandler):
    googs = [
        {
            'id': 1,
            'name': 'java开发',
            'author': 'chaoren',
            'price': '15000'
        },
        {
            'id': 2,
            'name': 'python开发',
            'author': 'chaoren2',
            'price': '14000'
        },
        {
            'id': 3,
            'name': 'h5开发',
            'author': 'chaoren3',
            'price': '14000'
        }
    ]
    action_map = {
        1: "取消订单",
        2: "再次购买",
        3: "评价"
    }
    def query(self, order_id):
        for item in self.googs:
            if item.get('id') == order_id:
                return item

    def get(self, order_id, action_code):
        self.write('订单查询')
        html = """
            <p>
                商品编号: %s
            </p>
            <p>
                商品名称: %s
            </p>
            <p>
                商品作者: %s
            </p>
            <p>
                商品价格: %s
            </p>      
        """
        goods = self.query(int(order_id))
        self.write(html % (goods.get('id'), goods.get('name'), goods.get('author'), goods.get('price') ))
        self.write(self.action_map.get(int(action_code)))

def make_app():
    return tornado.web.Application([
        ('/',IndexHandler),
        ('/search', SearchHandler),
        ('/cookie', CookieHandler),
        ('/order/(\d+)/(\d+)', OrderHandler)
    ], default_host=tornado.options.options.host)

if __name__ == "__main__":
    tornado.options.define('port',default=8000,type=int,help='bind socket port')
    tornado.options.define('host', default='localhost', type=str, help='设置host name')
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(tornado.options.options.port)
    print('starting http://%s:%s'% (tornado.options.options.host,tornado.options.options.port))
    tornado.ioloop.IOLoop.current().start()