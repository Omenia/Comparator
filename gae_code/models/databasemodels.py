# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class Grocery(ndb.Model):
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    price = ndb.FloatProperty()
    quantity = ndb.StringProperty()
    amount = ndb.FloatProperty()


class Shop(ndb.Model):
    """Models an individual shop"""
    name = ndb.StringProperty()
    city = ndb.StringProperty()
    area = ndb.StringProperty()
    postal_code = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now=True)
    price = ndb.FloatProperty()
    groceries = ndb.StructuredProperty(Grocery, repeated=True)

    @classmethod
    def query_book(cls, order = 'Halvin', qo = None):
        if order == 'Halvin':
            price_order = cls.price
        else:
            price_order = -cls.price
        if qo:
            return cls.query(qo).order(price_order)
        else:
            return cls.query().order(price_order)