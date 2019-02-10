from functools import wraps
from random import randrange
from time import sleep

from foobartory.errors import StockMissingError


class Stock:    # TODO: uuid
    foo = 0
    bar = 0
    foobar = 0
    money = 0


def _change_activity(new_activity):
    @wraps(new_activity)
    def wrapper(self, *args, **kwargs):
        if self.current_activity is not None and self.current_activity != new_activity.__name__:
            Robot.wait(5)
        self.current_activity = new_activity.__name__
        return new_activity(self, *args, **kwargs)

    return wrapper


class Robot:
    DURATION_MODIFIER = 1
    stock = Stock()

    def __init__(self):
        self.current_activity = None

    @classmethod
    def wait(cls, duration):
        sleep(duration * cls.DURATION_MODIFIER)

    @_change_activity
    def mine_foo(self):
        self.wait(1)
        self.stock.foo += 1

    @_change_activity
    def mine_bar(self):
        self.wait(randrange(5, 20) / 10)
        self.stock.bar += 1

    @_change_activity
    def assemble_foobar(self):
        if not (self.stock.foo and self.stock.bar):
            raise StockMissingError()
        self.wait(2)
        self.stock.bar -= 1
        if randrange(100) < 60:
            self.stock.foo -= 1
            self.stock.foobar += 1

    @_change_activity
    def sell_foobars(self, nb_to_sell):
        if nb_to_sell > self.stock.foobar:
            raise StockMissingError()
        if not (1 <= nb_to_sell <= 5):
            raise ValueError()
        self.wait(10)
        self.stock.foobar -= nb_to_sell
        self.stock.money += nb_to_sell

    @_change_activity
    def buy_robot(self):
        if not (self.stock.foo >= 6 and self.stock.money >= 3):     # TODO Stock manage errors
            raise StockMissingError()
        self.stock.foo -= 6
        self.stock.money -= 3
        return Robot()





