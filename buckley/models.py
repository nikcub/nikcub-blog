import sys, datetime, logging
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from buckley.datatypes import HtmlFromMarkdownProperty

class Post(db.Model):
	author = db.UserProperty()
	title = db.StringProperty(required=True)
	excerpt = db.StringProperty(multiline=True)
	content = db.TextProperty()
	content_html = HtmlFromMarkdownProperty(source = content, default = None)
	post_type = db.StringProperty(choices = set(['post', 'page']))
	status = db.StringProperty(required = True, choices = set(['draft', 'scheduled', 'published']))
	categories = db.ListProperty(db.Category)
	stub = db.StringProperty()
	pubdate = db.DateTimeProperty(auto_now_add=True)
	
	def create_new(title, content, categories = []):
		
		cats = []
		for category in categories:
			cats.append(db.Category(category))
			
		post = Post(
			title = title,
			excerpt = content[:250],
			content = content, 
			status = "draft",
			categories = cats,
			stub = self.get_stub(title),
			author = users.get_current_user(), 
			post_type = "post",
			pubdate = datetime.datetime.now()
		)
		
		try:
			post.put()
		except CapabilityDisabledError:
			return false
		return true 
	
	def update(self, values):
		for arg in values:
			if hasattr(self, arg) and values[arg] != getattr(self, arg):
				setattr(self, arg, values[arg])
		try:
			z = self.put()
			return True
		except CapabilityDisabledError:
			logging.error('yep')
	
	@classmethod
	def get_posts_published(self, num = 5):
		# query = db.Query(Post).filter('post_type = 'post'').order('-pubdate')
		query = self.all().filter('post_type = ', 'post').filter('status = ', 'published').order('-pubdate')
		return query.fetch(num)

	@classmethod
	def get_all(self, num = 5):
		# query = db.Query(Post).filter('post_type = 'post'').order('-pubdate')
		query = self.all().order('-pubdate')
		return query.fetch(num)
			
	@classmethod
	def get_last(self, num = 5):
		# query = db.Query(Post).filter('post_type = 'post'').order('-pubdate')
		query = self.all().filter('post_type = ', 'post').filter('status = ', 'published').order('-pubdate')
		# query.filter('limit 5')
		# query.order('-pubdate')
		return query.fetch(num)
			
	@classmethod
	def get_month(month, year):
		if not month:
			month = datetime.datetime.now().month
		if not year:
			year = datetime.datetime.now().year
	
	@classmethod
	def stub_exists(self, stub = ''):
		query = db.GqlQuery("select * from Post where stub = :1", stub)
		post = query.fetch(1)
		if query.count() == 0:
			return False
		return post
	
	@classmethod
	def is_key(self, k):
		try:
			query = db.get(db.Key(k))
		except:
			return False
		return True
	
	@classmethod
	def is_slug(self, key):
		return self.stub_exists(key)
	
	@classmethod
	def get_single_by_key(self, key):
		return db.get(db.Key(key))

	@classmethod
	def get_single_by_stub(self, stub):
		query = db.GqlQuery("select * from Post where stub = :1", stub)
		# query.filter('limit 5')
		# query.order('-pubdate')
		return query.fetch(1)

	@classmethod
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

	
	def get_stub(self, title, inc = 1):
		logging.info("Called with %s and %d" % (title, inc))
		stub_exists = Post.stub_exists(self.slugify(title))
		if stub_exists == False:
			return self.slugify(title)
		else:
			inc = inc + 1
			if inc > 2:
				return self.get_stub("%s-%d" % (self.slugify(title[:-2]), inc), inc)
			else:
				return self.get_stub("%s-%d" % (self.slugify(title), inc), inc)

	def slugify(self, value):
	    value = re.sub('[^\w\s-]', '', value).strip().lower()
	    return re.sub('[-\s]+', '-', value)
				
class Categories(db.Model):
	name = db.StringProperty(required=True)
