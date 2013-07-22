# -*- coding: utf-8 -*-

import urllib2
import webapp2
import jinja2

from models import *
from google.appengine.api import users

TEMPLATE_DIR = 'html_templates/'
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


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

    def __create_selected_values_dictionary(self, cities, areas, postal_codes, no_of_shops):
        selected_values = {}
        default_for_city = 'Kaupunki'
        default_for_area = 'Alue'
        default_for_no_of_shops = '5'
        default_for_postal_code = 'Postinumero'
        selected_values.update(self.__add_key_to_the_selected_values_dict('city', default_for_city))
        selected_values.update(self.__add_key_to_the_selected_values_dict('area', default_for_area))
        selected_values.update(self.__add_key_to_the_selected_values_dict('no_of_shops', default_for_no_of_shops, default_for_no_of_shops))
        selected_values.update(self.__add_key_to_the_selected_values_dict('postal_code', default_for_postal_code))

        if len(cities) != 0:
        #TODO: nice bubblegum here.
            cities.insert(0,default_for_city)
            areas.insert(0,default_for_area)
            postal_codes.insert(0,default_for_postal_code)
            no_of_shops.insert(0,default_for_no_of_shops)

        return selected_values, cities, areas, postal_codes, no_of_shops

    def __add_key_to_the_selected_values_dict(self, ident, default_id, default_value=''):
        selected_value = {}
        if self.request.get(ident):
            selected_value[ident] = self.request.get(ident)
            selected_value[ident+'_value'] = self.request.get(ident)
        else:
            selected_value[ident] = default_id
            selected_value[ident+'_value'] = default_value

        return selected_value

    def __generate_filters(self):
        no_of_shops = ['20', '50', '100']
        cities, areas, postal_codes = self.__get_cities_and_postal_codes()
        selected_values, cities, areas, postal_codes, no_of_shops = \
            self.__create_selected_values_dictionary(cities, areas, postal_codes, no_of_shops)

        filters = [Filter(name = 'order',
                        selected= 'Halvin',
                        selected_value='Halvin',
                        options= [
                            Opt(value='Kallein', name='Kallein'),
                            ]),
                    Filter(name='city',
                           selected=selected_values['city'],
                           selected_value=selected_values['city_value'],
                                options=self.__create_options_for_filter(cities)),
                    Filter(name='area',
                           selected=selected_values['area'],
                           selected_value=selected_values['area_value'],
                                options=self.__create_options_for_filter(areas)),
                    Filter(name='no_of_shops',
                           selected=selected_values['no_of_shops'],
                           selected_value=selected_values['no_of_shops_value'],
                                options=self.__create_options_for_filter(no_of_shops)),
                    Filter(name='postal_code',
                           selected=selected_values['postal_code'],
                           selected_value=selected_values['postal_code_value'],
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
