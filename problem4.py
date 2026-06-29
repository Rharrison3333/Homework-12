import random
import time
from graphics import *


class Die:
    def roll(self):
        return random.randint(1, 6)


class DiceSet:
    def __init__(self):
        self.dice = [Die() for _ in range(5)]

    def roll(self, number):
        values = []
        for i in range(number):
            values.append(self.dice[i].roll())
        return values


class TextInterface:
    def show_message(self, message):
        print(message)

    def show_roll(self, roll):
        print("Roll:", roll)

    def pause(self):
        input("Press Enter to continue.")


class GraphicsInterface:
    def __init__(self):
        self.win = GraphWin("Ship, Captain and Crew", 500, 300)
        self.win.setCoords(0, 0, 10, 10)

        self.title = Text(Point(5, 9), "")
        self.title.draw(self.win)

        self.roll_text = Text(Point(5, 5), "")
        self.roll_text.draw(self.win)

    def show_message(self, message):
        self.title.setText(message)
        time.sleep(1)

    def show_roll(self, roll):
        self.roll_text.setText("Roll: " + str(roll))
        time.sleep(1)

    def pause(self):
        self.win.getMouse()

    def close(self):
        self.win.close()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self, interface):
        dice = DiceSet()

        needed = 6
        dice_left = 5
        cargo = 0

        interface.show_message(self.name + "'s turn")

        for roll_number in range(3):
            roll = dice.roll(dice_left)
            interface.show_roll(roll)

            if needed in roll:
                roll.remove(needed)

                if needed == 6:
                    needed = 5
                elif needed == 5:
                    needed = 4
                elif needed == 4:
                    needed = 0

                dice_left -= 1

            if needed == 0:
                cargo = sum(roll)
                dice_left = 2

        if needed != 0:
            cargo = 0

        self.score = cargo
        interface.show_message(self.name + " scored " + str(self.score))


class Game:
    def __init__(self, players, interface):
        self.interface = interface
        self.players = []

        for i in range(players):
            self.players.append(Player("Player " + str(i + 1)))

    def play(self):
        winners = self.players

        while len(winners) > 1:
            for player in winners:
                player.take_turn(self.interface)

            highest = max(player.score for player in winners)

            winners = []

            for player in self.players:
                if player.score == highest:
                    winners.append(player)

            if len(winners) > 1:
                self.interface.show_message("Tie! Rolling again.")

        self.interface.show_message(winners[0].name + " wins!")
        self.interface.pause()


def main():
    players = int(input("Enter number of players: "))

    choice = input("Choose interface (text/graphics): ").lower()

    if choice == "graphics":
        interface = GraphicsInterface()
    else:
        interface = TextInterface()

    game = Game(players, interface)
    game.play()

    if choice == "graphics":
        interface.close()


main()
