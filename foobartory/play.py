from random import randint

from foobartory.robot import Robot


def pick_robot(robots):
    return robots[randint(0, len(robots) - 1)]


def play():
    Robot.DURATION_MODIFIER = 0.01
    robots = [Robot(), Robot()]
    while len(robots) < 3:
        if len(Robot.stock.foo) >= 3 and Robot.stock.money >= 6:
            robots.append(pick_robot(robots).buy_robot())
        if len(Robot.stock.foobar) == 5:
            pick_robot(robots).sell_foobars(5)
        if len(Robot.stock.foo) >= 1 and len(Robot.stock.bar) >= 1:
            pick_robot(robots).assemble_foobar()
        pick_robot(robots).mine_foo()
        pick_robot(robots).mine_bar()
    print('you won')


if __name__ == '__main__':
    play()
