# -*- coding: utf-8 -*-


import jinja2

from google.appengine.ext import ndb
from __init__ import return_user_and_login_url
from __init__ import create_basket


jinja_environment = jinja2.Environment(
                    loader=jinja2.FileSystemLoader('html_templates/'))


def render_shop_page_from_the_template(request, response, safe_url, page, chtml = None):
    url, url_linktext, user = return_user_and_login_url(request.uri)
    shop = ndb.Key(urlsafe=safe_url).get()
    template_values = {
        'shop': shop,
        'user': user,
        'url': url,
        'captchahtml': chtml,
        'url_linktext': url_linktext,
        'current_url': request.host.split(':')[0]
    }
    template = jinja_environment.get_template(page)
    response.out.write(template.render(template_values))


def render_add_shop(request, response, chtml):
    url, url_linktext, user = return_user_and_login_url(request.uri)
    template = jinja_environment.get_template('add_shop.html')
    groceries = create_basket()
    template_values = {
            'current_url': request.host.split(':')[0],
            'url': url,
            'user': user,
            'url_linktext': url_linktext,
            'groceries': groceries,
            'captchahtml': chtml
            }
    response.out.write(template.render(template_values))