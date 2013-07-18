# -*- coding: utf-8 -*-

import webapp2
import jinja2
import urllib2


TEMPLATE_DIR = 'html_templates/'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

USER = None

from models import *
from google.appengine.ext import ndb
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):

    def get(self):

        shops_to_show = self.__create_shops_which_are_shown()
        url, url_linktext, user = self.__return_user_and_login_url()
        filters = self.__generate_filters()
        template_values = {
          'shops_to_show': shops_to_show,
          'url': url,
          'url_linktext': url_linktext,
          'user': user,
          'filters': filters
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

    def post(self):

        if self.request.get('add_shop'):
            return self.redirect('/add_shop')
        elif self.request.get('apply_filter'):
            return self.redirect(self.__generate_url_with_filters())
        elif self.request.get('clear_filter'):
            return self.redirect('/')

    def __create_options_for_filter(self, opts):
        options = []
        for op in opts:
            options.append(Opt(value=op, name=op))
        return options

    def __generate_filters(self):
        cities, areas, postal_codes = self.__get_cities_and_postal_codes()
        filters = [Filter(name = 'order',
                        selected= 'Halvin',
                        selected_value='Halvin',
                        options= [
                            Opt(value='Kallein', name='Kallein'),
                            ]),
                    Filter(name='city',
                           selected='Kaupunki',
                           selected_value='',
                                options=self.__create_options_for_filter(cities)),
                    Filter(name='area',
                           selected='Alue',
                           selected_value='',
                                options=self.__create_options_for_filter(areas)),
                    Filter(name='no_of_shops',
                           selected='5',
                           selected_value='5',
                                options=self.__create_options_for_filter(['20', '50', '100'])),
                    Filter(name='postal_code',
                           selected='Postinumero',
                           selected_value='',
                                options=self.__create_options_for_filter(postal_codes))
                            ]
        return filters

    def __create_shops_which_are_shown(self):
        amount_of_shops = 5
        orde = 'Halvin'
        if self.request.get('order'):
            orde = self.request.get('order')
        if self.request.get('no_of_shops'):
            amount_of_shops = int(self.request.get('no_of_shops'))
        if self.request.get('area'):
            shops_to_show = Shop.query_book(order=orde, qo=Shop.area == self.request.get('area')).fetch(amount_of_shops)
        elif self.request.get('postal_code'):
            shops_to_show = Shop.query_book(order=orde, qo=Shop.postal_code == self.request.get('postal_code')).fetch(amount_of_shops)
        elif self.request.get('city'):
            shops_to_show = Shop.query_book(order=orde, qo=Shop.city == self.request.get('city')).fetch(amount_of_shops)
        else:
            shops_to_show = Shop.query_book(order=orde).fetch(amount_of_shops)
        return shops_to_show

    def __return_user_and_login_url(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Kirjaudu ulos'.decode('utf-8')
            user = users.get_current_user()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Kirjaudu sisään'.decode('utf-8')
            user = None
        return url, url_linktext, user

    def __get_cities_and_postal_codes(self):
        #TODO: This is nasty and costly one. We are just fetching all shops from the DB.
        shops = Shop.query_book().fetch(1000)
        cities = []
        postal_codes = []
        areas = []
        for shop in shops:
            if shop.city not in cities:
                cities.append(shop.city)
            if shop.area not in areas:
                areas.append(shop.area)
            if shop.postal_code not in postal_codes:
                postal_codes.append(shop.postal_code)
        return sorted(cities), sorted(areas), sorted(postal_codes)

    def __generate_url_with_filters(self):
        url_components = []
        if self.request.get('order'):
            url_components.append('order=' + self.request.get('order'))
        if self.request.get('city'):
            url_components.append('city=' + urllib2.quote(self.request.get('city').encode('utf8')))
        if self.request.get('area'):
            url_components.append('area=' + urllib2.quote(self.request.get('area').encode('utf8')))
        if self.request.get('no_of_shops'):
            url_components.append('no_of_shops=' + self.request.get('no_of_shops'))
        if self.request.get('postal_code'):
            url_components.append('postal_code=' + self.request.get('postal_code'))
        return '/?' + "&".join(url_components)


class AddShop(webapp2.RequestHandler):

    def get(self):
        if not users.get_current_user():
            return self.redirect('/')
        template = jinja_environment.get_template('add_shop.html')
        self.response.out.write(template.render())

    def post(self):
        self.__add_shop_to_database()
        return self.redirect('/')

    def __add_shop_to_database(self):
        shop = Shop(name=self.request.get('name'),
                    area=self.request.get('area'),
                    city=self.request.get('city'),
                    postal_code=self.request.get('postal_code'),
                    groceries=[self.__add_grocery_to_shop('Rasvaton Maito', 'rasvaton_maito', quantity='l', amount=1),
                               self.__add_grocery_to_shop('Reissumies', 'reissumies', quantity='kpl', amount=4,
                                                          manufacturer='Oululainen'),
                               self.__add_grocery_to_shop('Oltermanni', 'oltermanni', quantity='kg', amount=1,
                                                          manufacturer='Valio'),
                               self.__add_grocery_to_shop('Tomaatit', 'tomaatit', quantity='kg', amount=1,
                                                          manufacturer='Suomalainen'),
                               self.__add_grocery_to_shop('Naudan Jauheliha', 'jauheliha', quantity='g', amount=400),
                               self.__add_grocery_to_shop('Jogurtti', 'jogurtti', quantity='l', amount=1,
                                                          manufacturer='Arla & Ingman'),
                               self.__add_grocery_to_shop('Tutti-Frutti', 'tutti-frutti', quantity='g', amount=400,
                                                          manufacturer='Fazer'),
                               self.__add_grocery_to_shop('Juhlamokka Kahvi', 'kahvi', quantity='g', amount=500,
                                                          manufacturer='Paulig')
                               ]
        )
        shop.price = get_basket_price_from_groceries(shop.groceries)
        shop.put()

    def __add_grocery_to_shop(self, grocery_name, grocery_id, manufacturer = None, price = None, quantity = None, amount = None):
        return Grocery(name=grocery_name,
                       manufacturer=self.__return_value_to_the_grocery('manufacturer', manufacturer, grocery_id),
                       price=self.__format_number_with_dot(self.__return_value_to_the_grocery('price', price, grocery_id)),
                       quantity=self.__return_value_to_the_grocery('quantity', quantity, grocery_id),
                       amount=self.__format_number_with_dot(self.__return_value_to_the_grocery('amount', amount, grocery_id))
                       )

    def __format_number_with_dot(self, number):
        if isinstance(number, int):
            return float(number)
        else:
            return float(number.replace(',', '.'))

    def __return_value_to_the_grocery(self, info, value, grocery_id):
        if value:
            return value
        else:
            return self.request.get(grocery_id+'_'+info)


class ShowShop(webapp2.RequestHandler):

    def get(self):
        safe_url = self.request.get('shop')
        render_shop_page_from_the_template(self.response, safe_url, 'show_shop.html')

    def post(self):
        shop = ndb.Key(urlsafe = self.request.get('shop')).get()

        if self.request.get('delete_shop'):
            if not users.get_current_user():
                return self.redirect('/')
            shop.key.delete()
            return self.redirect('/')
        elif self.request.get('edit_shop'):
            return self.redirect('/edit_shop?shop='+shop.key.urlsafe())


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