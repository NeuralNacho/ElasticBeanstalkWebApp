from flask import request, jsonify
from flask import Blueprint
from .othello_game import OthelloGame
from .game_info_functions import *
import copy
import time

number_of_nodes = 0
othello_blueprint = Blueprint('othello_blueprint', __name__)

@othello_blueprint.route('/get_move', methods=['POST'])
def get_move():
    if request.method == 'POST':
        # Get the data sent in the request's JSON body
        data = request.json
        board = data.get('board')
        board = get_numpy_board(board)
        current_player = data.get('current_player')
        current_player = 1 if current_player == 'black' else 2

        # Generate a move
        global number_of_nodes
        number_of_nodes = 0
        depth = 7
        start_time = time.time()
        # final_eval, move = minimax_evaluation(board, current_player, depth)
        final_eval, move = alpha_beta_move(board, current_player, depth, float('-inf'), float('inf'))
        print('Time = ', time.time() - start_time)
        print('Number of nodes = ', number_of_nodes)
        print('Evaluation = ', final_eval, '\n')
        col = move % 8
        row = (move - col) / 8
        move = [row, col]
        return jsonify({"move": move})
    else:
        return jsonify({"error": "Invalid request method"})

def heuristic_evaluation(board):
    evaluation = 0  # Positive is good for black
    no_empty_spaces = 0
    for index in range(64):
        if board[index] == 0:
            no_empty_spaces += 1

    corners = [0, 7, 56, 63]
    for corner in corners:
        if board[corner] == 1:
            evaluation += 7
        elif board[corner] == 2:
            evaluation -= 7

    X_squares = [9, 14, 47, 54]
    for index in range(4):
        corner = corners[index]
        if board[corner] != 0:
            # Also checking corner not already filled otherwise no point counting 
            # this X square
            break
        square = X_squares[index]
        if board[square] == 1:
            evaluation -= 2
        elif board[square] == 2:
            evaluation += 2
    
    if no_empty_spaces > 20:
        no_black_moves = len(find_legal_moves(board, 1))
        evaluation += no_black_moves
        no_white_moves = len(find_legal_moves(board, 2))
        evaluation -= no_white_moves

    elif no_empty_spaces > 10:
        no_black_moves = len(find_legal_moves(board, 1))
        evaluation += no_black_moves
        no_white_moves = len(find_legal_moves(board, 2))
        evaluation -= no_white_moves
        for index in range(64):
            if board[index] == 1:
                evaluation += 1
            elif board[index] == 2:
                evaluation -= 1

    else: # In this case there are <= 10 moves left
        for index in range(64):
            if board[index] == 1:
                evaluation += 1
            elif board[index] == 2:
                evaluation -= 1

    return evaluation

def alpha_beta_move(board, current_player, depth, alpha, beta):
    # This function just returns the move 
    global number_of_nodes
    number_of_nodes += 1
    best_move = None
    
    legal_moves = find_legal_moves(board, current_player)
    if current_player == 1:
        # In this case, we want to maximise the evaluation
        eval = float('-inf')
        for move in legal_moves:
            board_copy = np.copy(board)
            new_board, new_player = handle_legal_move(board_copy, current_player, move)
            eval_of_current_move = alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta)
            if eval_of_current_move > eval:
                best_move = move
                eval = eval_of_current_move
            alpha = max(alpha, eval)
            # Update alpha. Black is guaruteed at least this evaluation.
            # Then this can be used in next iteration of loops as new alpha
            if alpha >= beta:
# To explain alpha > beta: For the very starting position we know black is guarunteed
# a score of at least alpha while white is guarunteed less than beta. So cannot have
# alpha > beta
# eval >= beta should give same result. Explanation: This means in response to the 
# white move black has a move with a higher eval than white's current best move (beta)
                break
        return eval, best_move
    else:
        eval = float('inf')
        for move in legal_moves:
            board_copy = np.copy(board)
            new_board, new_player = handle_legal_move(board_copy, current_player, move)
            eval_of_current_move = alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta)
            if eval_of_current_move < eval:
                best_move = move
                eval = eval_of_current_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return eval, best_move

def alpha_beta_evaluation(board, current_player, depth, alpha, beta):
    # This function just returns the eval
    global number_of_nodes
    number_of_nodes += 1
    if depth == 0:
        eval = heuristic_evaluation(board)
        return eval

    legal_moves = find_legal_moves(board, current_player)
    if len(legal_moves) == 0: # Deal with passing turns here
        current_player = 1 if current_player == 2 else 2
        legal_moves = find_legal_moves(board, current_player)
        if len(legal_moves) == 0: # In this case, game is over
            black_white_difference = 0 # no black discs minus no white discs
            for index in range(64):
                if board[index] == 1:
                    black_white_difference += 1
                elif board[index] == 2:
                    black_white_difference -= 1
            if black_white_difference > 0:
                return float('inf')
            elif black_white_difference < 0:
                return float('-inf')
            else:
                return 0
        # If len(legal_moves) != 0 then the function will continue executing
        # current_player already swapped above

    if current_player == 1:
        # In this case, we want to maximise the evaluation
        eval = float('-inf')
        for move in legal_moves:
            board_copy = np.copy(board)
            new_board, new_player = handle_legal_move(board_copy, current_player, move)
            eval = max(eval, alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta))
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return eval
    else:
        eval = float('inf')
        for move in legal_moves:
            board_copy = np.copy(board)
            new_board, new_player = handle_legal_move(board_copy, current_player, move)
            eval = min(eval, alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta))
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return eval

def minimax_evaluation(board, current_player, depth):
    global number_of_nodes
    number_of_nodes += 1
    best_move = None
    # Using this to test alpha_beta
    if depth == 0:
        # 2 turns passed means game is over (including situation where board is full)
        eval = heuristic_evaluation(board)
        return eval, ''
    
    legal_moves = find_legal_moves(board, current_player)
    if current_player == 1:
        max_eval = float('-inf')
        for move in legal_moves:
            board_copy = np.copy(board)
            new_board, new_player = handle_legal_move(board_copy, current_player, move)
            new_eval, _ = minimax_evaluation(new_board, new_player, depth - 1)
            if new_eval > max_eval:
                best_move = move
                max_eval = new_eval
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board_copy = np.copy(board)
            new_board, new_player = handle_legal_move(board_copy, current_player, move)
            new_eval, _ = minimax_evaluation(new_board, new_player, depth - 1)
            if new_eval < min_eval:
                best_move = move
                min_eval = new_eval
        return min_eval, best_move