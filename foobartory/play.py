from random import randint

from foobartory.robot import Robot


def pick_robot(robots):
    return robots[randint(0, len(robots) - 1)]


def play():
    Robot.DURATION_MODIFIER = 0.01
    Robot.robots += [Robot(), Robot()]
    while len(Robot.robots) < 30:
        for robot in Robot.robots.copy():
            robot.next_activity()
    print('you won')


if __name__ == '__main__':
    play()
