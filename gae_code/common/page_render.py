# -*- coding: utf-8 -*-


import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from __init__ import return_user_and_login_url


jinja_environment = jinja2.Environment(
                    loader=jinja2.FileSystemLoader('html_templates/'))


def render_shop_page_from_the_template(request, response, safe_url, page):
    url, url_linktext, user = return_user_and_login_url(request.uri)
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
        'current_url': request.host.split(':')[0]
    }
    template = jinja_environment.get_template(page)
    response.out.write(template.render(template_values))


def render_add_shop(request, response):
    url, url_linktext, user = return_user_and_login_url(request.uri)
    template = jinja_environment.get_template('add_shop.html')
    template_values = {
            'current_url': request.host.split(':')[0],
            'url,': url,
            'user': user,
            'url_linktext': url_linktext
            }
    response.out.write(template.render(template_values))
