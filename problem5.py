from graphics import *
import time


class Ball:
    def __init__(self, win, x, y, radius, velocity):
        self.win = win
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.gravity = -9.8
        self.bounce_factor = 0.75

        self.circle = Circle(Point(self.x, self.y), self.radius)
        self.circle.draw(self.win)

    def update(self, dt):
        old_y = self.y

        self.velocity = self.velocity + self.gravity * dt
        self.y = self.y + self.velocity * dt

        if self.y <= self.radius:
            self.y = self.radius
            self.velocity = -self.velocity * self.bounce_factor

        dy = self.y - old_y
        self.circle.move(0, dy)

    def is_moving(self):
        return abs(self.velocity) > 0.1 or self.y > self.radius + 0.01


def main():
    height = float(input("Enter starting height: "))

    win = GraphWin("Three Bouncing Balls", 600, 600)
    win.setCoords(0, 0, 10, 10)

    ground = Line(Point(0, 0), Point(10, 0))
    ground.draw(win)

    balls = [
        Ball(win, 3, height, 0.3, 0),
        Ball(win, 5, height * 0.8, 0.3, 2),
        Ball(win, 7, height * 0.6, 0.3, 4)
    ]

    dt = 0.05

    while True:
        moving = False

        for ball in balls:
            ball.update(dt)

            if ball.is_moving():
                moving = True

        time.sleep(dt)

        if not moving:
            break

    message = Text(Point(5, 5), "All three balls stopped bouncing.")
    message.draw(win)

    win.getMouse()
    win.close()


main()
