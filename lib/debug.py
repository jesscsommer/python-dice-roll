from classes.puzzle import Puzzle
from classes.player import Player
from classes.result import Result
from random import sample

Result.drop_table()
Player.drop_table()
Puzzle.drop_table()

Player.create_table()
Puzzle.create_table()
Result.create_table()

player_1 = Player.create('Winnr')
player_2 = Player.create('Loser')

# p1 = Puzzle.create_puzzle("Matte")
# p2 = Puzzle.create_puzzle("snake")

# #  def __init__(self, player_id, puzzle_id, score = 0, num_guesses = 0, id = None):

# r1 = Result.create(player_1.id, p1.id, 0, 6)
# r2 = Result.create(player_2.id, p2.id, 300, 1)


# for num in range(1, 18):
#     Result.create(player_1.id, pm.id, num, sample([1, 2, 3, 4, 5], 1)[0])

print('complete')
import ipdb; ipdb.set_trace()