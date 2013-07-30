# -*- coding: utf-8 -*-


import webapp2


from google.appengine.api import users
from google.appengine.ext import ndb
from common import render_shop_page_from_the_template


class ShowShop(webapp2.RequestHandler):

    def get(self):
        safe_url = self.request.get('shop')
        render_shop_page_from_the_template(self.request, self.response, safe_url, 'show_shop.html')

    def post(self):
        shop = ndb.Key(urlsafe = self.request.get('shop')).get()

        if self.request.get('delete_shop'):
            if not users.get_current_user():
                return self.redirect('/')
            shop.key.delete()
            return self.redirect('/')
        elif self.request.get('edit_shop'):
            return self.redirect('/edit_shop?shop='+shop.key.urlsafe())