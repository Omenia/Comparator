# -*- coding: utf-8 -*-


import webapp2


from mainpage import MainPage
from addshop import AddShop
from showshop import ShowShop
from editpage import EditShop


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_shop', AddShop),
    ('/show_shop', ShowShop),
    ('/edit_shop', EditShop)
])
