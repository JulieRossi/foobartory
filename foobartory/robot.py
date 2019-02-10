from functools import wraps
from random import randrange, choice
from time import sleep
from uuid import uuid4

from foobartory.errors import StockMissingError


class Stock:
    def __init__(self):
        self.foo = []
        self.bar = []
        self.foobar = []
        self.money = 0


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
    robots = []

    def __init__(self):
        self.current_activity = None

    @classmethod
    def wait(cls, duration):
        sleep(duration * cls.DURATION_MODIFIER)

    @_change_activity
    def mine_foo(self):
        self.wait(1)
        self.stock.foo.append(uuid4())

    @_change_activity
    def mine_bar(self):
        self.wait(randrange(5, 20) / 10)
        self.stock.bar.append(uuid4())

    @_change_activity
    def assemble_foobar(self):
        if not (self.stock.foo and self.stock.bar):
            raise StockMissingError()
        self.wait(2)
        bar = self.stock.bar.pop()
        if randrange(100) < 60:
            foo = self.stock.foo.pop()
            self.stock.foobar.append('{}-{}'.format(foo, bar))

    @_change_activity
    def sell_foobars(self, nb_to_sell):
        if nb_to_sell > len(self.stock.foobar):
            raise StockMissingError()
        if not (1 <= nb_to_sell <= 5):
            raise ValueError()
        self.wait(10)
        self.stock.foobar = self.stock.foobar[:-nb_to_sell]
        self.stock.money += nb_to_sell

    @_change_activity
    def buy_robot(self):
        if not (len(self.stock.foo) >= 6 and self.stock.money >= 3):     # TODO Stock manage errors
            raise StockMissingError()
        self.stock.foo = self.stock.foo[:-6]
        self.stock.money -= 3
        self.robots.append(Robot())

    def next_activity(self):
        if len(self.stock.foo) >= 6 and self.stock.money >= 3:
            self.buy_robot()
        elif len(self.stock.foobar) == 5:
            self.sell_foobars(5)
        elif len(self.stock.foo) >= 5 and len(self.stock.bar) >= 5:
            self.assemble_foobar()
        elif self.current_activity == self.mine_foo.__name__ and len(self.stock.foo) < 10:
            self.mine_foo()
        elif self.current_activity == self.mine_bar.__name__ and len(self.stock.bar) < 10:
            self.mine_bar()
        else:
            choice([self.mine_foo, self.mine_bar])()
