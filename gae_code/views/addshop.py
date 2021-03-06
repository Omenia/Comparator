# -*- coding: utf-8 -*-

import webapp2
import logging
try:
    from common import get_basket_price_from_groceries
    from common import render_page
    from common import identifier
    from recaptcha.client import captcha
    from google.appengine.api import users
    from models import Grocery
    from models import Shop
    from common import create_basket
except ImportError:
    pass

class AddShop(webapp2.RequestHandler):

    def get(self):
        chtml = captcha.create_capthca_html()
        render_page(self.request, self.response, 'add_shop.html', chtml)

    def post(self):
        if not users.get_current_user():
            correct_captcha, error = captcha.create_rechatpca(self.request)
            if correct_captcha:
                self.__add_shop_to_database()
                return self.redirect('/')
            else:
                #TODO: Now this only display page that CAPTCHA was incorrect
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.write(error)

        else:
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
        self.__recalculate_price_classes(shop)

    def __recalculate_price_classes(self, newShop):
        # Get all shops in DB and append the newly added shop.
        shops = Shop.query_book().fetch()
        shops.append(newShop)
        prices = []

        # Get a list of all prices
        for shop in shops:
            prices.append(shop.price)
        
        # Sort prices in ascending order
        prices.sort()
        
        # Define low and high price ranges
        lowPrice = 0.0
        highPrice = 0.0        
        if(len(prices) > 0):
            minPrice = min(prices)
            maxPrice = max(prices)
            diff = maxPrice - minPrice
            lowPrice = minPrice+0.25*diff
            highPrice = minPrice+0.75*diff
       
        # Assign new price class and price index for every shop
        priceIndex = 1
        for shop in shops:
            if shop.price < lowPrice:
                shop.priceClass = 1
            elif shop.price > highPrice:
                shop.priceClass = 3
            else:
                shop.priceClass = 2
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
               manufacturer=self._grocery_value('manufacturer',
                             manufacturer,
                             grocery_id
                             ),
               price=self._dotify(self._grocery_value('price',
                            price,
                            grocery_id)
                            ),
               quantity=self._grocery_value('quantity',
                            quantity,
                            grocery_id),
               amount=self._dotify(self._grocery_value(
                            'amount',
                            amount, grocery_id))
               )

    def _dotify(self, number):
        if isinstance(number, int):
            return float(number)
        else:
            return float(number.replace(',', '.'))

    def _grocery_value(self, info, value, grocery_id):
        if value:
            return value
        else:
            return self.request.get(grocery_id + '_' + info)
