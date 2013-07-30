# -*- coding: utf-8 -*-


import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from __init__ import return_user_and_login_url


jinja_environment = jinja2.Environment(
                    loader=jinja2.FileSystemLoader('html_templates/'))


def render_shop_page_from_the_template(current_url, response, safe_url, page):
    url, url_linktext, user = return_user_and_login_url(current_url)
    if users.get_current_user():
        user = users.get_current_user()
    else:
        user = None
    shop = ndb.Key(urlsafe=safe_url).get()
    template_values = {
        'shop': shop,
        'user': user,
        'url,': url,
        'url_linktext': url_linktext,
        'current_url': current_url
    }
    template = jinja_environment.get_template(page)
    response.out.write(template.render(template_values))


def render_add_shop(current_url, response):
    url, url_linktext, user = return_user_and_login_url(current_url)
    template = jinja_environment.get_template('add_shop.html')
    template_values = {
            'current_url': current_url,
            'url,': url,
            'user': user,
            'url_linktext': url_linktext
            }
    response.out.write(template.render(template_values))
