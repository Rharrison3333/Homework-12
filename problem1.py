import random


class Die:
    def __init__(self):
        self.sides = ["L", "C", "R", ".", ".", "."]

    def roll(self):
        return random.choice(self.sides)


class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 3

    def has_chips(self):
        return self.chips > 0

    def take_chip(self):
        self.chips -= 1

    def give_chip(self):
        self.chips += 1


class Pot:
    def __init__(self):
        self.chips = 0

    def add_chip(self):
        self.chips += 1

    def empty_pot(self):
        amount = self.chips
        self.chips = 0
        return amount


class LCRGame:
    def __init__(self, number_of_players):
        self.players = []
        self.die = Die()
        self.pot = Pot()

        for i in range(number_of_players):
            self.players.append(Player("Player " + str(i + 1)))

    def active_players(self):
        count = 0

        for player in self.players:
            if player.has_chips():
                count += 1

        return count

    def show_status(self):
        for player in self.players:
            print(player.name, "has", player.chips, "chips.")

        print("Center pot has", self.pot.chips, "chips.")
        print()

    def play_turn(self, player_number):
        player = self.players[player_number]

        print(player.name + "'s turn")

        if player.chips == 0:
            print(player.name, "has no chips and skips.")
            return

        dice_to_roll = player.chips

        if dice_to_roll > 3:
            dice_to_roll = 3

        rolls = []

        for i in range(dice_to_roll):
            rolls.append(self.die.roll())

        print("Rolls:", rolls)

        for roll in rolls:
            if roll == "L":
                left = (player_number - 1) % len(self.players)
                player.take_chip()
                self.players[left].give_chip()
            elif roll == "R":
                right = (player_number + 1) % len(self.players)
                player.take_chip()
                self.players[right].give_chip()
            elif roll == "C":
                player.take_chip()
                self.pot.add_chip()

    def find_winner(self):
        for player in self.players:
            if player.chips > 0:
                return player

    def play_game(self):
        round_number = 1

        while self.active_players() > 1:
            print("Round", round_number)

            for i in range(len(self.players)):
                if self.active_players() == 1:
                    break

                self.play_turn(i)
                self.show_status()

            round_number += 1

        winner = self.find_winner()
        winner.chips += self.pot.empty_pot()

        print(winner.name, "wins the game!")
        print(winner.name, "receives the center pot.")
        self.show_status()


def main():
    number_of_players = int(input("Enter number of players: "))

    while number_of_players < 3:
        print("LCR needs at least 3 players.")
        number_of_players = int(input("Enter number of players: "))

    game = LCRGame(number_of_players)
    game.play_game()


main()
