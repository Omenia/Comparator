# -*- coding: utf-8 -*-


import webapp2
import jinja2

from mainpage import MainPage
from addshop import AddShop
from showshop import ShowShop
from editpage import EditShop


TEMPLATE_DIR = 'html_templates/'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

USER = None


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_shop', AddShop),
    ('/show_shop', ShowShop),
    ('/edit_shop', EditShop)
])
