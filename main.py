# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

TEMPLATE_DIR = 'html_templates/'
USER = None

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
    postal_code = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.FloatProperty()
    groceries  = ndb.StructuredProperty(Grocery, repeated=True)

    @classmethod
    def query_book(cls, qo = None):
        if qo:
            return cls.query(qo).order(cls.price)
        else:
            return cls.query().order(cls.price)


class MainPage(webapp2.RequestHandler):
    shops_to_show = 5

    def get(self):
        cities = []
        postal_codes = []

        if self.request.get('no_of_shops'):
            self.shops_to_show = int(self.request.get('no_of_shops'))
        shops = Shop.query_book().fetch(self.shops_to_show)
        if self.request.get('postal_code'):
            shops_to_show = Shop.query_book(Shop.postal_code == self.request.get('postal_code')).fetch(self.shops_to_show)
        elif self.request.get('city'):
            shops_to_show = Shop.query_book(Shop.city == self.request.get('city')).fetch(self.shops_to_show)
        else:
            shops_to_show = Shop.query_book().fetch(self.shops_to_show)

        if users.get_current_user():
          url = users.create_logout_url(self.request.uri)
          url_linktext = 'Ulos Kirjautuminen'
          user = users.get_current_user()
        else:
          url = users.create_login_url(self.request.uri)
          url_linktext = 'Kirjautuminen'
          user = None

        for shop in shops:
            if shop.city not in cities:
                cities.append(shop.city)
            if shop.postal_code not in postal_codes:
                postal_codes.append(shop.postal_code)
        sorted(cities)
        sorted(postal_codes)
        template_values = {
          'shops_to_show': shops_to_show,
          'shops': shops,
          'url': url,
          'url_linktext': url_linktext,
          'cities': cities,
          'user': user,
          'postal_codes': postal_codes
        }


        template = jinja_environment.get_template(TEMPLATE_DIR+'index.html')
        self.response.out.write(template.render(template_values))

    def post(self):

        if self.request.get('add_shop'):
            return self.redirect('/add_shop')
        elif self.request.get('apply_filter'):
            url = []
            if self.request.get('city'):
                url.append('city='+self.request.get('city'))
            if self.request.get('no_of_shops'):
                url.append('no_of_shops='+self.request.get('no_of_shops'))
            if self.request.get('postal_code'):
                url.append('postal_code='+self.request.get('postal_code'))
            return self.redirect('/?'+"&".join(url))
        elif self.request.get('clear_filter'):
            return self.redirect('/')


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
                    postal_code=self.request.get('postal_code'),
                    groceries=[self.__add_grocery_to_shop('Rasvaton Maito', 'rasvaton_maito', quantity='l', amount=1),
                               self.__add_grocery_to_shop('Reissumies', 'reissumies', quantity='kpl', amount=4,
                                                          manufacturer='Oululainen'),
                               self.__add_grocery_to_shop('Oltermanni', 'oltermanni', quantity='kg', amount=1,
                                                          manufacturer='Valio'),
                               self.__add_grocery_to_shop('Tomaatit', 'tomaatit', quantity='kg', amount=1,
                                                          manufacturer='Suomalainen'),
                               self.__add_grocery_to_shop('Jauheliha', 'jauheliha', quantity='g', amount=400),
                               self.__add_grocery_to_shop('Jogurtti', 'jogurtti', quantity='l', amount=1,
                                                          manufacturer='Arla & Ingman'),
                               self.__add_grocery_to_shop('Tutti-Frutti', 'tutti-frutti', quantity='g', amount=400,
                                                          manufacturer='Fazer')
                               ]
        )
        shop.price = get_basket_price_from_groceries(shop.groceries)
        shop.put()

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
        shop.city = self.request.get('city')
        shop.postal_code = self.request.get('postal_code')
        for grocery in shop.groceries:
            grocery.price = float(self.request.get(grocery.name+"_price"))
            if grocery.name == ("Jauheliha" or "Tomaatit" or "Rasvaton Maito"):
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


def get_basket_price_from_groceries(groceries):
    price = 0
    for grocery in groceries:
        price += grocery.price
    return price

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_shop', AddShop),
    ('/show_shop', ShowShop),
    ('/edit_shop', EditShop)
])