import random
import time
from graphics import *


class Die:
    def __init__(self):
        self.sides = ["L", "C", "R", ".", ".", "."]

    def roll(self):
        return random.choice(self.sides)


class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 3


class Pot:
    def __init__(self):
        self.chips = 0


class TextInterface:
    def show_message(self, message):
        print(message)

    def show_status(self, players, pot):
        for player in players:
            print(player.name, "has", player.chips, "chips.")
        print("Center pot has", pot.chips, "chips.")
        print()

    def pause(self):
        input("Press Enter to continue.")


class GraphicsInterface:
    def __init__(self):
        self.win = GraphWin("LCR Game", 500, 400)
        self.win.setCoords(0, 0, 10, 10)
        self.text = Text(Point(5, 8), "")
        self.text.draw(self.win)
        self.status = Text(Point(5, 5), "")
        self.status.draw(self.win)

    def show_message(self, message):
        self.text.setText(message)
        time.sleep(1)

    def show_status(self, players, pot):
        status_text = ""

        for player in players:
            status_text += player.name + ": " + str(player.chips) + " chips\n"

        status_text += "Center pot: " + str(pot.chips)
        self.status.setText(status_text)
        time.sleep(1)

    def pause(self):
        self.win.getMouse()

    def close(self):
        self.win.close()


class LCRGame:
    def __init__(self, number_of_players, interface):
        self.players = []
        self.die = Die()
        self.pot = Pot()
        self.interface = interface

        for i in range(number_of_players):
            self.players.append(Player("Player " + str(i + 1)))

    def active_players(self):
        count = 0

        for player in self.players:
            if player.chips > 0:
                count += 1

        return count

    def play_turn(self, player_number):
        player = self.players[player_number]

        self.interface.show_message(player.name + "'s turn")

        if player.chips == 0:
            self.interface.show_message(player.name + " has no chips and skips.")
            return

        dice_to_roll = player.chips

        if dice_to_roll > 3:
            dice_to_roll = 3

        rolls = []

        for i in range(dice_to_roll):
            rolls.append(self.die.roll())

        self.interface.show_message("Rolls: " + str(rolls))

        for roll in rolls:
            if roll == "L":
                left = (player_number - 1) % len(self.players)
                player.chips -= 1
                self.players[left].chips += 1
            elif roll == "R":
                right = (player_number + 1) % len(self.players)
                player.chips -= 1
                self.players[right].chips += 1
            elif roll == "C":
                player.chips -= 1
                self.pot.chips += 1

    def find_winner(self):
        for player in self.players:
            if player.chips > 0:
                return player

    def play_game(self):
        round_number = 1

        while self.active_players() > 1:
            self.interface.show_message("Round " + str(round_number))

            for i in range(len(self.players)):
                if self.active_players() == 1:
                    break

                self.play_turn(i)
                self.interface.show_status(self.players, self.pot)

            round_number += 1

        winner = self.find_winner()
        winner.chips += self.pot.chips
        self.pot.chips = 0

        self.interface.show_message(winner.name + " wins!")
        self.interface.show_status(self.players, self.pot)
        self.interface.pause()


def main():
    number_of_players = int(input("Enter number of players: "))

    while number_of_players < 3:
        print("LCR needs at least 3 players.")
        number_of_players = int(input("Enter number of players: "))

    choice = input("Text or graphics interface? ")

    if choice.lower() == "graphics":
        interface = GraphicsInterface()
    else:
        interface = TextInterface()

    game = LCRGame(number_of_players, interface)
    game.play_game()

    if choice.lower() == "graphics":
        interface.close()


main()
