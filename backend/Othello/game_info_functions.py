import numpy as np

def get_numpy_board(board):
    # will have board s.t. 0 is empty 1 is black 2 is white
    numpy_board = np.zeros(64, dtype = int)
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'black':
                numpy_board[row*8 + col] = 1
            elif board[row][col] == 'white':
                numpy_board[row*8 + col] = 2
    return numpy_board

def is_valid_move(board, current_player, index):
    if board[index] != 0:
        return False
    
    directions = [-9, -8, -7, # top left to bottom right
                  -1,      1,
                   7,  8,  9]
    for direction in directions:
        new_index = index + direction
        found_opponent_piece = False
        while 0 <= new_index < 64:
            if board[new_index] == 0:
                break
            if board[new_index] != current_player:
                found_opponent_piece = True
                new_index += direction
                continue
            if found_opponent_piece: 
                # Must have also met a disc of current player
                return True
            else:
                # Have found disc of current player without 
                # finding opponent piece
                break

def find_legal_moves(board, current_player):
    legal_moves = []
    for index in range(64):
        if board[index] == 0 and is_valid_move(board, current_player, index):
            legal_moves.append(index)
    return legal_moves

def handle_legal_move(board, current_player, move_index):
    board[move_index] = current_player
    flip_discs(board, current_player, move_index)
    current_player = 1 if current_player == 2 else 2
    return board, current_player

def flip_discs(board, current_player, move_index):
    directions = [-9, -8, -7, # top left to bottom right
                  -1,      1,
                   7,  8,  9]
    for direction in directions:
        discs_to_flip = []
        new_index = move_index + direction
        while 0 <= new_index < 64:
            if board[new_index] == 0:
                break
            if board[new_index] != current_player:
                discs_to_flip.append(new_index)
                new_index += direction
                continue
            if board[new_index] == current_player:
                for disc in discs_to_flip:
                    board[disc] = current_player
                break