from Othello.game_info_functions import *
from Othello.get_othello_move import heuristic_evaluation
# from Othello.neural_network_evaluation import *
import numpy as np
import time

board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         ['black', 'white', 'white', 'white', 'black', 'black', 'black', 'black']]

game_state = get_game_state(board, 2)
print(heuristic_evaluation(game_state))

bitboard_black = np.random.randint(2, size = (8, 8, 1)).astype(np.float32)
bitboard_white = np.random.randint(2, size = (8, 8, 1)).astype(np.float32)
position = (bitboard_black, bitboard_white)
print(np.array(position))

