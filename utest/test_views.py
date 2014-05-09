from unittest import TestCase
from addshop import AddShop

class TestViews(TestCase):
    def setUp(self):
        self.a = AddShop()
    def test_dotifying(self):
        self.assertEqual(self.a._dotify("4,2"), 4.2)
    def test_grocery_value(self):
        self.assertEqual(self.a._grocery_value("", "foo", ""), "foo")
