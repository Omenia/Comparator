# -*- coding: utf-8 -*-


def get_basket_price_from_groceries(groceries):
    #TODO: this function is also in addshop.py
    price = 0
    for grocery in groceries:
        price += grocery.price
    return price
