# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

TEMPLATE_DIR = 'html_templates/'

from google.appengine.ext import ndb
from google.appengine.api import users


class Grocery(ndb.Model):
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    price = ndb.FloatProperty()
    quantity = ndb.StringProperty()
    amount = ndb.FloatProperty()


class Shop(ndb.Model):
    """Models an individual shop"""
    name = ndb.StringProperty()
    city = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.FloatProperty()
    groceries  = ndb.StructuredProperty(Grocery, repeated=True)

    @classmethod
    def query_book(cls):
        return cls.query().order(cls.price)


class MainPage(webapp2.RequestHandler):
    def get(self):
        shops = Shop.query_book().fetch(5)

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


        template = jinja_environment.get_template(TEMPLATE_DIR+'index.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        if self.request.get('add_shop'):
            return self.redirect('/add_shop')


class AddShop(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template(TEMPLATE_DIR+'add_shop.html')
        self.response.out.write(template.render())

    def post(self):
        self.__add_shop_to_database()
        return self.redirect('/')

    def __add_shop_to_database(self):
        shop = Shop(name=self.request.get('name'),
                    city=self.request.get('city'),
                    groceries=[self.__add_grocery_to_shop('Rasvaton Maito', 'rasvaton_maito', quantity='l', amount=1),
                               self.__add_grocery_to_shop('Reissumies', 'reissumies', quantity='kpl', amount=4,
                                                          manufacturer='Oululainen'),
                               self.__add_grocery_to_shop('Oltermanni', 'oltermanni', quantity='kg', amount=1,
                                                          manufacturer='Valio'),
                               self.__add_grocery_to_shop('Tomaatit', 'tomaatit', quantity='kg', amount=1),
                               self.__add_grocery_to_shop('Jauheliha', 'jauheliha', quantity='g', amount=400)
                               ]
        )
        shop.price = self.__get_basket_price_from_groceries(shop.groceries)
        shop.put()

    def __get_basket_price_from_groceries(self, groceries):
        price = 0
        for grocery in groceries:
            price += grocery.price
        return price

    def __add_grocery_to_shop(self, grocery_name, grocery_id, manufacturer = None, price = None, quantity = None, amount = None):
        return Grocery(name=grocery_name,
                       manufacturer=self.__return_value_to_the_grocery('manufacturer', manufacturer, grocery_id),
                       price=float(self.__return_value_to_the_grocery('price', price, grocery_id)),
                       quantity=self.__return_value_to_the_grocery('quantity', quantity, grocery_id),
                       amount=float(self.__return_value_to_the_grocery('amount', amount, grocery_id))
                       )

    def __return_value_to_the_grocery(self, info, value, grocery_id):
        if value:
            return value
        else:
            print grocery_id+'_'+info + ":" + self.request.get(grocery_id+'_'+info)
            return self.request.get(grocery_id+'_'+info)


class ShowShop(webapp2.RequestHandler):

    def get(self):
        safe_url = self.request.get('shop')
        render_shop_page_from_the_template(self.response, safe_url, TEMPLATE_DIR+'show_shop.html')

    def post(self):
        shop = ndb.Key(urlsafe = self.request.get('shop')).get()

        if self.request.get('delete_shop'):
            shop.key.delete()
            return self.redirect('/')
        elif self.request.get('edit_shop'):
            return self.redirect('/edit_shop?shop='+shop.key.urlsafe())


class EditShop(webapp2.RequestHandler):
    def get(self):
        safe_url = self.request.get('shop')
        render_shop_page_from_the_template(self.response, safe_url, TEMPLATE_DIR+'edit_shop.html')

    def post(self):
        shop = ndb.Key(urlsafe = self.request.get('shop')).get()
        shop.name = self.request.get('name')
        shop.put()
        return self.redirect('/show_shop?shop='+shop.key.urlsafe())


def render_shop_page_from_the_template(response, safe_url, page):
    shop = ndb.Key(urlsafe = safe_url).get()
    template_values = {
        'shop': shop
    }

    template = jinja_environment.get_template(page)
    response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_shop', AddShop),
    ('/show_shop', ShowShop),
    ('/edit_shop', EditShop)
])