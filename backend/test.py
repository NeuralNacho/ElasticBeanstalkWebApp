from Othello.game_info_functions import *
import time
import cProfile

board = [['black','white',0      ,'white','white','white','white','white'],
         [0      ,'white','white','white',0      ,0      ,0,0],
         ['white',0      ,'white',0      ,'white',0      ,0,0],
         [0      ,0      ,'white',0      ,0      ,'white',0,0],
         [0      ,0      ,'white',0      ,0      ,0      ,'white',0],
         [0      ,0      ,      0,0      ,0      ,0      ,0,'white'],
         [0      ,0      ,'white',0      ,0      ,0      ,0,0],
         [0      ,0      ,'white',0      ,0      ,0      ,0,0]]
black_start, white_start = get_bitboards(board)
game_state = OthelloGameState(black_start, white_start, 1)
legal_moves = find_legal_moves(game_state)
test_move = legal_moves & -legal_moves
print_bitboard(test_move)
print('\n')
game_state = handle_legal_move(game_state, test_move)
print_bitboard(game_state.black_bitboard)
print('\n')
print_bitboard(game_state.white_bitboard)
