import random


class Die:
    def roll(self):
        return random.randint(1, 6)


class DiceSet:
    def __init__(self):
        self.dice = [Die() for i in range(5)]

    def roll(self, number):
        rolls = []

        for i in range(number):
            rolls.append(self.dice[i].roll())

        return rolls


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self):
        dice = DiceSet()

        needed = 6
        dice_left = 5
        cargo_score = 0

        print()
        print(self.name, "turn")

        for roll_number in range(1, 4):
            input("Press Enter to roll.")

            roll = dice.roll(dice_left)
            print("Roll", roll_number, ":", roll)

            if needed in roll:
                roll.remove(needed)

                if needed == 6:
                    print("Ship found")
                    needed = 5
                elif needed == 5:
                    print("Captain found")
                    needed = 4
                elif needed == 4:
                    print("Crew found")
                    needed = 0

                dice_left -= 1

            if needed == 0:
                cargo_score = sum(roll)
                print("Cargo:", roll)
                print("Current cargo score:", cargo_score)
                dice_left = 2

        if needed != 0:
            cargo_score = 0

        self.score = cargo_score
        print(self.name, "final score:", self.score)


class ShipCaptainCrewGame:
    def __init__(self, players):
        self.players = []

        for i in range(players):
            self.players.append(Player("Player " + str(i + 1)))

    def play(self):
        winners = self.players

        while len(winners) > 1:
            for player in winners:
                player.take_turn()

            highest = max(player.score for player in winners)

            winners = []

            for player in self.players:
                if player.score == highest:
                    winners.append(player)

            if len(winners) > 1:
                print()
                print("Tie! Rolling again...")

        print()
        print(winners[0].name, "wins!")


def main():
    players = int(input("Enter number of players: "))

    while players < 2:
        players = int(input("Enter at least 2 players: "))

    game = ShipCaptainCrewGame(players)
    game.play()


main()
