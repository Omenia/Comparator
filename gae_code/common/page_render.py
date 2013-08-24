# -*- coding: utf-8 -*-


import jinja2

from google.appengine.ext import ndb
from __init__ import return_user_and_login_url
from __init__ import create_basket


jinja_environment = jinja2.Environment(
                    loader=jinja2.FileSystemLoader('html_templates/'))


def render_page(request, response, page, chtml = None, safe_url = None):
    url, url_linktext, user = return_user_and_login_url(request.uri)
    template_values = {
        'user': user,
        'url': url,
        'url_linktext': url_linktext,
        'current_url': request.host.split(':')[0]
    }
    if safe_url:
        shop = ndb.Key(urlsafe=safe_url).get()
        template_values['shop'] = shop
    if chtml:
        template_values['captchahtml'] = chtml
    if page == 'add_shop.html':
        groceries = create_basket()
        template_values['groceries'] = groceries

    template=jinja_environment.get_template(page)
    response.out.write(template.render(template_values))
