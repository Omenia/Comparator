# -*- coding: utf-8 -*-


import webapp2

from recaptcha.client import captcha
from os import environ
from google.appengine.api import users
from google.appengine.ext import ndb
from common import render_page


class ShowShop(webapp2.RequestHandler):

    def get(self):
        chtml = captcha.create_capthca_html
        safe_url = self.request.get('shop')
        render_page(self.request,
                    self.response,
                    'show_shop.html',
                    chtml,
                    safe_url
                    )

    def post(self):
        shop = ndb.Key(urlsafe = self.request.get('shop')).get()
        if not users.get_current_user():
                challenge = self.request.get('recaptcha_challenge_field')
                response = self.request.get('recaptcha_response_field')
                remoteip = environ['REMOTE_ADDR']
                cResponse = captcha.submit(
                         challenge,
                         response,
                         "6LewluUSAAAAAC-nDS0rxfqrq8e6-ZzrknKJBhNf",
                         remoteip)
                if cResponse.is_valid:
                    print "!!!!!!!!s"
                    if self.request.get('delete_shop'):
                        print "!?!"
                        shop.key.delete()
                        return self.redirect('/')
                    elif self.request.get('edit_shop'):
                        print "!?!?"
                        return self.redirect('/edit_shop?shop='+shop.key.urlsafe())
                else:
                    #TODO: Now this only display page that CAPTCHA was incorrect
                    error = cResponse.error_code
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.write(error)
        else:
            if self.request.get('delete_shop'):
                shop.key.delete()
                return self.redirect('/')
            elif self.request.get('edit_shop'):
                return self.redirect('/edit_shop?shop='+shop.key.urlsafe())
