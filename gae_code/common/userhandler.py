# -*- coding: utf-8 -*-

from google.appengine.api import users


def return_user_and_login_url(request_uri):
    if users.get_current_user():
        url = users.create_logout_url(request_uri)
        url_linktext = 'Kirjaudu ulos'.decode('utf-8')
        user = users.get_current_user()
    else:
        url = users.create_login_url(request_uri)
        url_linktext = 'Kirjaudu sisään'.decode('utf-8')
        user = None
    return url, url_linktext, user
