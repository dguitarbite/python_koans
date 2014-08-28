#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

# from runner.koan import *
import random


class DiceSet(object):
    def __init__(self):
        self.values = list()
        self.number_count = dict()
        self.cumulative_score = 0

    def get_values(self):
        return self.values

    def get_number_count(self):
        return self.number_count

    def roll(self, no_dice=5):
        '''This is used to generate the effect of rolling a dice.

        1. Random Roll:
            If values == 0, then random roll for the number of dices rolled.

        2. Custom Roll:
            If values != 0 then roll the values.
        '''
        self.values = list()
        # Random Roll
        for i in range(no_dice):
            self.values.append(random.randint(1, 6))

        # Calculate the score for the current roll
        score = self._count_number()
        return score

    def _count_number(self):
        '''Get the list of numbers rolled and return the total score as
        per the rules of the game.
        '''

        # Generate a dictonary containing the count of each number for
        # the given roll.
        self.number_count = {}.fromkeys(self.values, 0)
        self.number_score = {}.fromkeys(self.values, 0)

        for d in self.values:
            self.number_count[d] += 1

        turn_score = self._get_score()
        self.cumulative_score += turn_score

        if self.cumulative_score < 300:
            return self.cumulative_score

        elif turn_score == 0:
            return 0

        else:
            # Count Number of Zeroes in the score
            zeroes = self.number_score.values().count(0)
            if zeroes == 0:
                self.roll(5)
            else:
                self.roll(zeroes)

    def _get_score(self):
        '''Scoring Table is given below. These rules will be applied

            Three 1's => 1000 points
            Three 6's =>  600 points
            Three 5's =>  500 points
            Three 4's =>  400 points
            Three 3's =>  300 points
            Three 2's =>  200 points
            One   1   =>  100 points
            One   5   =>   50 points

        '''

        try:
            # A set of three ones is 1000 points
            self.number_score[1] += (self.number_count[1] // 3) * 1000
        except Exception:
            pass

        try:
            # A one ( ! 3 x ones) is worth 100 points.
            self.number_score[1] += (self.number_count[1] % 3) * 100
        except Exception:
            pass

        try:
            # A five (that is not part of set of three) is worth 50 pints
            self.number_score[5] += (self.number_count[5] % 3) * 50
        except Exception:
            pass

        # A set of three self.number_count (! ones)
        # is worth 100 times the number
        for no in range(2, 7):
            try:
                self.number_score[no] += (self.number_count[no] // 3) * 100 * no
            except Exception:
                pass

        turn_score = sum(self.number_score.values())
        return turn_score


class Greed(object):
    '''This class has the flow and rules of the GREED game.

        total_score: (Global Var)
            Total Score of a player
        round_score: (Local Var)
            Score of the complete round
        cumulative_score: (Local Var)
            Sum total of all the turns
        turn_score: (Local Var)
            Score of the every turn

        Flow of the Game:
            Rounds:

                Turns:
                    1. If new turn: Roll the Dice
                       elif: turn_score >= 300 points, Roll
                       else: exit the round.

                    2. If the turn_score is not zero
                        Roll the non-scoring dice(s) again.
                       else: turn_score == 0
                        Accumulated Score = 0
                        end round

                    3. If all the five are scoring dice >> New Turn.

                    4. If the player decides to stop:
                        total_score = total_score + accumulated_score
                        end round.

            End Game:

                1. Total_Score >= 3000 == go to final round
                2. Only one Round -- Compare Accumulated Score,
                    get winner
    '''

    def __init__(self, players=2):

        # Initialize player names
        self.players = list()
        self.init_players(players)
        self.total_score = dict()
        self.init_total_score()
        self.winner = str()

    def get_winner(self):
        return self.winner

    def get_players(self):
        return self.players

    def init_players(self, no_players):
        '''Initialize player names.'''

        for no_player in range(no_players):
            self.players.append('player' + str(no_player + 1))

    def init_total_score(self):
        self.total_score = {}.fromkeys(self.players, 0)

    def rounds(self):
        '''Start a round. A single round contains multiple turns.'''

        # end_game = False
        i = 0
        while i < 10:
            for player in self.players:
                self.turn(player)
                # end_game = True
            i += 1

        self.final_round()

    def turn(self, player):
        '''Start a turn.'''
        dice_set = DiceSet()
        round_score = dice_set.roll(5)
        try:
            self.total_score[player] += round_score
        except Exception:
            pass

        return self.total_score[player]

    # TODO(Required?): Decide if we need this or not!
    def final_round(self):
        '''Final Round turn.'''

        self.init_total_score()

        for player in self.players:
            self.turn(player)

        winner_score = max(self.total_score.values())
        for name, score in self.total_score.items():
            if score == winner_score:
                self.winner = name

        print("Winner is:", self.winner)
        print("Winner is", winner_score)

"""
class AboutExtraCredit(Koan):
    '''Test cases for Extra Credits exercise in koans. This is totally written
    by us, now that I think of it its totally written by me ... go figure out
    who me is.
    '''

    def test_extra_credit_task(self):
        '''Dunno what is this!'''

        # self.assertTrue()
        pass

    def test_basic_scores_should_pass(self):
        '''Basic Set of tests run as per the given table below

            Basic Tests

            Throw       Score
            ---------   ------------------
            5 1 3 4 1   50 + 2 * 100 = 250
            1 1 1 3 1   1000 + 100 = 1100
            2 4 4 5 4   400 + 50 = 450
        '''

        throw = [[5, 1, 3, 4, 1],
                 [1, 1, 1, 3, 1],
                 [2, 4, 4, 5, 4]]

        dice_stuff = DiceSet()
        self.assertEqual(dice_stuff.roll(throw[0]), 250)
        self.assertEqual(dice_stuff.roll(throw[1]), 1100)
        self.assertEqual(dice_stuff.roll(throw[2]), 450)

    def test_initialize_players_should_return_players(self):
        '''Initlaize Greed Object, and do initial basic tests.'''

        play_greed = Greed()
        play_greed_again = Greed(5)

        # Initialize Greed with default parameters
        self.assertEqual(['player1', 'player2'], play_greed.players())

        # Initialize Greed with custom paramerets
        self.assertEqual(
            ['player1', 'player2', 'player3', 'player4', 'player5'],
            play_greed_again.players())

"""
if __name__ == '__main__':

    greed = Greed(20)
    greed.rounds()
    print("The Winner is", greed.get_winner())
