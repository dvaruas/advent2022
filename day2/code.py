import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from enum import Enum

from utils import from_file


class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def get_score(self) -> int:
        match self:
            case self.ROCK:
                return 1
            case self.PAPER:
                return 2
            case self.SCISSORS:
                return 3

    def get_match_score(self, opponent_move) -> int:
        if opponent_move == self:
            # It is a draw
            return 3
        elif (
            (opponent_move == Move.ROCK and my_move == Move.SCISSORS)
            or (opponent_move == Move.SCISSORS and my_move == Move.PAPER)
            or (opponent_move == Move.PAPER and my_move == Move.ROCK)
        ):
            # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
            return 0
        else:
            # Wins the match
            return 6


class Outcome(Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2

    def get_score(self) -> int:
        match self:
            case self.WIN:
                return 6
            case self.LOSE:
                return 0
            case self.DRAW:
                return 3

    def get_needed_move(self, opponent_move: Move) -> Move:
        match self:
            case self.WIN:
                match opponent_move:
                    case Move.ROCK:
                        return Move.PAPER
                    case Move.PAPER:
                        return Move.SCISSORS
                    case Move.SCISSORS:
                        return Move.ROCK
            case self.LOSE:
                match opponent_move:
                    case Move.ROCK:
                        return Move.SCISSORS
                    case Move.PAPER:
                        return Move.ROCK
                    case Move.SCISSORS:
                        return Move.PAPER
            case self.DRAW:
                return opponent_move


def get_opponent_move(coded_move: str) -> Move:
    match coded_move:
        case "A":
            return Move.ROCK
        case "B":
            return Move.PAPER
        case "C":
            return Move.SCISSORS


# Thinks the coded_strategy is my move as per first part
def get_my_move(coded_strategy: str) -> Move:
    match coded_strategy:
        case "X":
            return Move.ROCK
        case "Y":
            return Move.PAPER
        case "Z":
            return Move.SCISSORS


# Thinks the coded_strategy is the play outcome desired as per second part
def get_my_desired_outcome(coded_strategy: str) -> Outcome:
    match coded_strategy:
        case "X":
            return Outcome.LOSE
        case "Y":
            return Outcome.DRAW
        case "Z":
            return Outcome.WIN


if __name__ == "__main__":
    strategy_guide_inputs = from_file.get_input_for(2)
    if strategy_guide_inputs == None:
        print("input not found")
        sys.exit(1)

    # Part 1 - According to first strategy
    my_score = 0
    for strategy_line in strategy_guide_inputs:
        opponent_move, my_move = strategy_line.split()
        opponent_move = get_opponent_move(opponent_move)
        my_move = get_my_move(my_move)

        my_score += my_move.get_score()
        my_score += my_move.get_match_score(opponent_move)

    # My total score according to first strategy
    print(my_score)

    # part 2 - According to second strategy
    my_score = 0
    for strategy_line in strategy_guide_inputs:
        opponent_move, my_desired_outcome = strategy_line.split()
        opponent_move = get_opponent_move(opponent_move)
        my_desired_outcome = get_my_desired_outcome(my_desired_outcome)

        my_move = my_desired_outcome.get_needed_move(opponent_move)
        my_score += my_move.get_score()
        my_score += my_desired_outcome.get_score()

    # My total score according to second strategy
    print(my_score)
