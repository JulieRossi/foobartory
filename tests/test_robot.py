from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import foobartory
from foobartory.errors import StockMissingError
from foobartory.robot import Robot, Stock


class BaseTest:
    @classmethod
    def teardown_class(cls):
        Robot.stock = Stock()
        Robot.robots = []


class TestMineFoo(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.mine_foo()

    def test_foo_created(self):
        assert len(Robot.stock.foo) == 1

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(1)])


class TestChangeActivityFromSameActivity(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.mine_foo()
        cls.robot.mine_foo()

    def test_foo_created(self):
        assert len(Robot.stock.foo) == 2

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(1), call(1)])


class TestChangeActivityFromAnotherActivity(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.current_activity = 'some_activity'
        cls.robot.mine_foo()

    def test_foo_created(self):
        assert len(Robot.stock.foo) == 1

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(5), call(1)])


class RandomCall:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __eq__(self, other):
        return self.start < other < self.stop


class TestMineBar(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.mine_bar()

    def test_bar_created(self):
        assert len(Robot.stock.bar) == 1

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(RandomCall(0.5, 2))])


@pytest.mark.skip('need to seed random')
class TestAssembleFooBarOk(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foo = ['uuid']
        cls.robot.stock.bar = ['uuid']
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.assemble_foobar()

    def test_bar_used(self):
        assert len(Robot.stock.bar) == 0

    def test_foo_used(self):
        assert len(Robot.stock.foo) == 0

    def test_foobar_created(self):
        assert len(Robot.stock.foobar) == 1

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(2)])


@pytest.mark.skip('need to seed random')
class TestFooBarUniqueID(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.mine_foo()
        cls.robot.mine_foo()
        cls.robot.mine_bar()
        cls.robot.mine_bar()
        cls.robot.assemble_foobar()
        cls.robot.assemble_foobar()

    def test_bar_used(self):
        assert Robot.stock.foobar[0] != Robot.stock.foobar[1]


class TestAssembleFooBarKoMissingBar(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foo = ['uuid']
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(StockMissingError):
            self.robot.assemble_foobar()


class TestAssembleFooBarKoMissingFoo(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.bar = ['uuid']
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(StockMissingError):
            self.robot.assemble_foobar()


class TestSellFooBarOk(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foobar = ['uuid'] * 5
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.sell_foobars(2)

    def test_foobar_used(self):
        assert len(Robot.stock.foobar) == 3

    def test_money_received(self):
        assert Robot.stock.money == 2

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(10)])


class TestSellFooBarOkExactAmount(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foobar = ['uuid'] * 5
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.sell_foobars(5)

    def test_foobar_used(self):
        assert len(Robot.stock.foobar) == 0

    def test_mony_received(self):
        assert Robot.stock.money == 5

    def test_duration(self):
        self.mocked_wait.assert_has_calls([call(10)])


class TestSellFooBarKoMissingFooBar(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foobar = ['uuid']
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(StockMissingError):
            self.robot.sell_foobars(2)


class TestSellFooBarKoNbToSellTooBig(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foobar = ['uuid'] * 10
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(ValueError):
            self.robot.sell_foobars(10)


class TestSellFooBarKoNbToSellTooSmall(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foobar = ['uuid'] * 10
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(ValueError):
            self.robot.sell_foobars(-1)


class TestBuyRobotOk(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foo = ['uuid'] * 10
        cls.robot.stock.money = 10
        cls.robot.DURATION_MODIFIER = 0.01
        cls.robot.buy_robot()

    def test_foobar_used(self):
        assert len(Robot.stock.foo) == 4

    def test_money_spent(self):
        assert Robot.stock.money == 7

    def test_robot_created(self):
        assert len(Robot.robots) == 1

    def test_duration(self):
        self.mocked_wait.assert_not_called()


class TestBuyRobotOkExactAmount(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foo = ['uuid'] * 6
        cls.robot.stock.money = 3
        cls.robot.DURATION_MODIFIER = 0.01
        cls.new_robot = cls.robot.buy_robot()

    def test_foobar_used(self):
        assert len(Robot.stock.foo) == 0

    def test_money_spent(self):
        assert Robot.stock.money == 0

    def test_robot_created(self):
        assert len(Robot.robots) == 1

    def test_duration(self):
        self.mocked_wait.assert_not_called()


class TestBueRobotKoMissingFoo(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foo = ['uuid']
        cls.robot.stock.money = 10
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(StockMissingError):
            self.robot.buy_robot()


class TestBuyRobotKoMissingMoney(BaseTest):
    @classmethod
    def setup_class(cls):
        cls.mocked_wait = MagicMock()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(foobartory.robot.Robot, 'wait', cls.mocked_wait)
        cls.robot = Robot()
        cls.robot.stock.foo = ['uuid'] * 10
        cls.robot.stock.money = 1
        cls.robot.DURATION_MODIFIER = 0.01

    def test_raises(self):
        with pytest.raises(StockMissingError):
            self.robot.buy_robot()
