# -*- coding: utf-8 -*-

import webapp2
import jinja2



TEMPLATE_DIR = 'html_templates/'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

USER = None

from views import *
from google.appengine.ext import ndb
from google.appengine.api import users



class EditShop(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            return self.redirect('/')
        safe_url = self.request.get('shop')
        render_shop_page_from_the_template(self.response, safe_url, 'edit_shop.html')

    def post(self):
        shop = ndb.Key(urlsafe = self.request.get('shop')).get()
        shop.name = self.request.get('name')
        shop.area = self.request.get('area')
        shop.city = self.request.get('city')
        shop.postal_code = self.request.get('postal_code')
        for grocery in shop.groceries:
            grocery.price = float(self.request.get(grocery.name+"_price"))
            if grocery.name == "Rasvaton Maito" or grocery.name == "Naudan Jauheliha":
                grocery.manufacturer = self.request.get(grocery.name+"_manufacturer")
        shop.price = get_basket_price_from_groceries(shop.groceries)
        shop.put()
        return self.redirect('/show_shop?shop='+shop.key.urlsafe())


def render_shop_page_from_the_template(response, safe_url, page):

    if users.get_current_user():
      user = users.get_current_user()
    else:
      user = None
    shop = ndb.Key(urlsafe = safe_url).get()
    template_values = {
        'shop': shop,
        'user': user
    }
    template = jinja_environment.get_template(page)
    response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_shop', AddShop),
    ('/show_shop', ShowShop),
    ('/edit_shop', EditShop)
])