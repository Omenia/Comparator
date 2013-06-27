# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import ndb
from google.appengine.api import users

class Grocery(ndb.Model):
    name = ndb.StringProperty()
    price = ndb.FloatProperty()

class Shop(ndb.Model):
  """Models an individual shop"""
  name = ndb.StringProperty()
  city = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)
  price = ndb.FloatProperty()
  groceries  = ndb.StructuredProperty(Grocery, repeated=True)

  @classmethod
  def query_book(cls):
    return cls.query().order(-cls.price)


class MainPage(webapp2.RequestHandler):
  def get(self):
    shops = Shop.query().fetch(5)

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


class Grocerybasket(webapp2.RequestHandler):
  def post(self):
    if self.request.get('add_shop'):
        shop = Shop(name=self.request.get('name'), city=self.request.get('city'), price=float(self.request.get('g1_price'))+float(self.request.get('g2_price')),
                    groceries=[Grocery(name = self.request.get('g1_name'),
                                      price = float(self.request.get('g1_price'))),
                               Grocery(name = self.request.get('g2_name'),
                                      price = float(self.request.get('g2_price')))])
        shop.put()
    elif self.request.get('delete_shop'):
        print "buu"
        shop_to_delete = Shop.query().fetch(1)
        shop_to_delete[0].key.delete()
    self.redirect('/')

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Grocerybasket)
])