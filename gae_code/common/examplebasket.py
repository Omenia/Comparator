from ident import identifier


class Grocery(object):
    def __init__(self, name, identi, manufacturer, quantity, amount):
        self.name = name
        self.identi = identi
        self.manufacturer = manufacturer
        self.quantity = quantity
        self.amount = amount


def create_basket():
    groceries = [__add_grocery('Suomalainen rasvaton maito', 1, 'l'),
                 __add_grocery('Suomalainen tomaatti', 1, 'kg'),
                 __add_grocery('Reissumies', 4, 'kpl', 'Oululainen'),
                 __add_grocery('Oltermanni', 1, 'kg', 'Valio'),
                 __add_grocery('Suomalainen naudan jauheliha', 400, 'g'),
                 __add_grocery('Juhla Mokka kahvi', 500, 'g', 'Paulig'),
                 __add_grocery('Maustettu jogurtti', 1, 'l', 'Arla Ingman'),
                 __add_grocery('Tutti Frutti Jumbo', 400, 'g', 'Fazer')
                 ]
    return groceries


def __add_grocery(name, amount, quantity, manufacturer=None):
    return Grocery(name=name,
            identi=identifier(name),
            manufacturer=manufacturer,
            amount=amount,
            quantity=quantity)
