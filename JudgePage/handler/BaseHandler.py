#coding=utf8
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    @property
    def baidu_resArrs(self):
        return self.application.baidu_resArrs
