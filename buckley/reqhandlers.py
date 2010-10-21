import os
import logging
import traceback
import sys
import cgi

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from config import config
import serialize
from application import *

class Base(webapp.RequestHandler):
	def __init__(self):
		self.conf = config('blog.yaml')
		
	def render(self, template_name, vars, response_code = 200, response_type = False):
		content = self.get_page(template_name, vars, response_type)
		self.response.clear()
		self.response.set_status(response_code)
		self.response.out.write(content)
	
	def render_error(self, message = False, code = 404):
		self.render('error', { 
			'code': '%d - %s' % (code, self.response.http_status_message(code)), 
			'message': message 
		}, code)

	def get_page(self, template_name, vars, response_type = False):
		if not response_type:
			response_type = self.get_response_type()
		vars = self.get_template_vars(vars)
		if response_type in ['xml', 'json']:
			serial_f = getattr(serialize, response_type)
			content = serial_f(vars)
			self.response.headers['Content-Type'] = "application/%s; charset=utf-8" % (response_type)
		else:
			content = template.render(self.get_template_path(template_name, response_type), vars)
		return content

	def get_template_vars(self, vars):
		additional = {
			'admin': users.is_current_user_admin(),
			'user': users.get_current_user(),
			'logout': users.create_logout_url('/'),
			'login': users.create_login_url('/'),
			'title': 'test'
			# 'title': self.conf_get('title')
		}
		return dict(zip(vars.keys() + additional.keys(), vars.values() + additional.values()));
	
	def get_template_path(self, template_name, template_format = 'html'):
		return os.path.join(os.path.dirname(__file__), '..', 'templates', template_name + '.' + template_format)
	
	def get_response_type(self):
		accept = self.request.headers['accept'].split(',')
		if accept[0] == 'application/json' or self.request.get('json'):
			return 'json'
		elif self.request.get('xml'):
			return 'xml'
		else:
			return 'html'
	
	def get_param_dict(self):
		params = {}
		for argument in self.request.arguments():
			params[argument] = self.request.get(argument)
		return params

	def handle_exception(self, exception, debug_mode):
		logging.exception(exception)
		message = "An error has occured"
		if debug_mode:
			lines = ''.join(traceback.format_exception(*sys.exc_info()))
			message = '<pre>%s</pre>' % (cgi.escape(lines, quote=True))
		self.render_error(message, 500)

	
class Admin(Base):
	def initialize(self, request, response):
		super(Admin, self).initialize(request, response)
		user = users.get_current_user()
		if not user or not users.is_current_user_admin():
			raise AppAuthError
			
	def is_admin():
		return users
		
	def get_template_path(self, template_name, template_format = 'html'):
		return os.path.join(os.path.dirname(__file__), 'templates', template_name + '.' + template_format)
	