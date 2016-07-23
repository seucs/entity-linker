#coding=utf8
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	@property
	def tables(self):
		return self.application.tables

	@property
	def db(self):
		return self.application.db

	def on_finish(self): 
		self.db.close() 
