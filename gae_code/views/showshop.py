# -*- coding: utf-8 -*-


import webapp2

from recaptcha.client import captcha
from google.appengine.api import users
from google.appengine.ext import ndb
from common import render_page
from recaptcha.client import captcha


class ShowShop(webapp2.RequestHandler):

    def get(self):
        chtml = captcha.create_capthca_html()
        safe_url = self.request.get('shop')
        render_page(self.request,
                    self.response,
                    'show_shop.html',
                    chtml,
                    safe_url
                    )

    def post(self):
        shop = ndb.Key(urlsafe=self.request.get('shop')).get()
        if not users.get_current_user():
                correct_captcha, error = captcha.create_rechatpca(self.request)
                if correct_captcha:
                        if self.request.get('delete_shop'):
                            shop.key.delete()
                            return self.redirect('/')
                        elif self.request.get('edit_shop'):
                            return self.redirect('/edit_shop?shop=' + shop.key.urlsafe())
                else:
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.write(error)
        else:
            if self.request.get('delete_shop'):
                shop.key.delete()
                return self.redirect('/')
            elif self.request.get('edit_shop'):
                return self.redirect('/edit_shop?shop='+shop.key.urlsafe())
