
import webapp2

from google.appengine.ext import ndb
from common import get_basket_price_from_groceries
from common import render_page


class EditShop(webapp2.RequestHandler):
    def get(self):
        safe_url = self.request.get('shop')
        render_page(
                    self.request,
                    self.response,
                    'edit_shop.html',
                    safe_url=safe_url
                    )

    def post(self):
        shop = ndb.Key(urlsafe=self.request.get('shop')).get()
        shop.name = self.request.get('name')
        shop.area = self.request.get('area')
        shop.city = self.request.get('city')
        shop.postal_code = self.request.get('postal_code')
        for grocery in shop.groceries:
            grocery.price = float(self.request.get(grocery.name + "_price"))
            if grocery.name == "Suomalainen rasvaton maito" or grocery.name == "Suomalainen naudan jauheliha":
                grocery.manufacturer = self.request.get(grocery.name + "_manufacturer")
        shop.price = get_basket_price_from_groceries(shop.groceries)
        shop.put()
        return self.redirect('/show_shop?shop=' + shop.key.urlsafe())
