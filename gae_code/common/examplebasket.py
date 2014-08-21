import os
from ident import identifier


class Grocery(object):
    def __init__(self, name, identi, manufacturer, quantity, amount):
        self.name = name
        self.identi = identi
        self.manufacturer = manufacturer
        self.quantity = quantity
        self.amount = amount


def create_basket():

    groceries = []

    print os.getcwd()
    with open('site/content.txt') as item:
        for line in item.readlines():
            groceries.append(__add_grocery(line.split('|')))

    return groceries


def __add_grocery(grocery):
    if len(grocery) < 4:
        grocery.append(None)
    return Grocery(name=grocery[0],
            identi=grocery[0],
            amount=grocery[1],
            quantity=grocery[2],
            manufacturer=grocery[3])
