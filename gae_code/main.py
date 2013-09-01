# -*- coding: utf-8 -*-


import webapp2
from views import MainPage
from views import AddShop
from views import ShowShop
from views import EditShop


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_shop', AddShop),
    ('/show_shop', ShowShop),
    ('/edit_shop', EditShop)
])
