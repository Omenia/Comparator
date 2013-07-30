
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from common import get_basket_price_from_groceries
from common import render_shop_page_from_the_template


class EditShop(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            return self.redirect('/')
        safe_url = self.request.get('shop')
        render_shop_page_from_the_template(
                self.request.host.split(':')[0], self.response, safe_url, 'edit_shop.html')

    def post(self):
        shop = ndb.Key(urlsafe=self.request.get('shop')).get()
        shop.name = self.request.get('name')
        shop.area = self.request.get('area')
        shop.city = self.request.get('city')
        shop.postal_code = self.request.get('postal_code')
        for grocery in shop.groceries:
            grocery.price = float(self.request.get(grocery.name + "_price"))
            if grocery.name == "Rasvaton Maito" or grocery.name == "Naudan Jauheliha":
                grocery.manufacturer = self.request.get(grocery.name + "_manufacturer")
        shop.price = get_basket_price_from_groceries(shop.groceries)
        shop.put()
        return self.redirect('/show_shop?shop=' + shop.key.urlsafe())

