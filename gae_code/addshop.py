# -*- coding: utf-8 -*-


import webapp2
from common import get_basket_price_from_groceries
from common import render_add_shop
from common import identifier


from google.appengine.api import users
from models import Grocery
from models import Shop
from common import create_basket


class AddShop(webapp2.RequestHandler):

    def get(self):
        if not users.get_current_user():
            return self.redirect('/')
        render_add_shop(self.request, self.response)

    def post(self):
        self.__add_shop_to_database()
        return self.redirect('/')

    def __add_shop_to_database(self):
        shop = Shop(name=self.request.get('name'),
                    area=self.request.get('area'),
                    city=self.request.get('city'),
                    postal_code=self.request.get('postal_code'),
                    groceries=self.__return_basket_from_form()
                            )
        shop.price = get_basket_price_from_groceries(shop.groceries)
        shop.put()

    def __return_basket_from_form(self):
        example_basket = create_basket()
        basket = []
        for grocery in example_basket:
            if grocery.name == "Suomalainen rasvaton maito" or grocery.name == "Suomalainen naudan jauheliha":
                basket.append(self.__add_grocery_to_shop(grocery.name,
                                           identifier(grocery.name),
                                           quantity=grocery.quantity,
                                           amount=grocery.amount))
            else:
                basket.append(self.__add_grocery_to_shop(grocery.name,
                                            identifier(grocery.name),
                                            quantity=grocery.quantity,
                                            amount=grocery.amount,
                                            manufacturer=grocery.manufacturer))
        return basket

    def __add_grocery_to_shop(self, grocery_name,
                              grocery_id,
                              manufacturer=None,
                              price=None, quantity=None,
                              amount=None):
        return Grocery(name=grocery_name,
                       manufacturer=self.__return_value_to_the_grocery(
                                                                'manufacturer',
                                                                manufacturer,
                                                                grocery_id
                                                                ),
                       price=self.__format_number_with_dot(
                                            self.__return_value_to_the_grocery(
                                            'price',
                                            price, grocery_id)
                                                           ),
                       quantity=self.__return_value_to_the_grocery(
                                                        'quantity',
                                                        quantity, grocery_id),
                       amount=self.__format_number_with_dot(
                                            self.__return_value_to_the_grocery(
                                                        'amount',
                                                        amount, grocery_id))
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
            return self.request.get(grocery_id + '_' + info)
