# -*- coding: utf-8 -*-


import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
                    loader=jinja2.FileSystemLoader('html_templates/'))



def render_shop_page_from_the_template(current_url, response, safe_url, page):
    #TODO: this function is also in showshop.py
    if users.get_current_user():
        user = users.get_current_user()
    else:
        user = None
    shop = ndb.Key(urlsafe=safe_url).get()
    template_values = {
        'shop': shop,
        'user': user,
        'current_url': current_url,
    }
    template = jinja_environment.get_template(page)
    response.out.write(template.render(template_values))
