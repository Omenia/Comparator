import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import ndb
from google.appengine.api import users


class Shop(ndb.Model):
  """Models an individual shop"""
  city = ndb.StringProperty()
  postal_code = ndb.StringProperty()
  city_area = ndb.StringProperty()
  #croceries  = ndb.StructuredProperty(Crocery, repeated=True)

  name = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_book(cls):
    return cls.query().order(-cls.date)


class MainPage(webapp2.RequestHandler):
  def get(self):
    shops = Shop.query_book().fetch(20)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Ulos Kirjautuminen'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Kirjautuminen'

    template_values = {
      'shops': shops,
      'url': url,
      'url_linktext': url_linktext
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):
  def post(self):
    shop = Shop(name = self.request.get('name'), city = self.request.get('city'))
    shop.put()
    self.redirect('/')

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook)
])