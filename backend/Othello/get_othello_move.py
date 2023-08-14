from flask import request, jsonify
from flask import Blueprint
from .game_info_functions import *
import time
import cProfile

number_of_nodes = 0
othello_blueprint = Blueprint('othello_blueprint', __name__)

@othello_blueprint.route('/get_move', methods=['POST'])
def get_move():
    if request.method == 'POST':
        # Get the data sent in the request's JSON body
        data = request.json
        board = data.get('board')
        current_player = data.get('current_player')
        current_player = 1 if current_player == 'black' else 2
        game_state = get_game_state(board, current_player)

        # Generate a move
        global number_of_nodes
        number_of_nodes = 0
        depth = 7
        start_time = time.time()
        final_eval, move = alpha_beta_move(game_state, depth, float('-inf'), float('inf'))
        # cProfile.runctx("alpha_beta_move(game_state, depth, float('-inf'), float('inf'))", globals(), locals())
        print('Time = ', time.time() - start_time)
        print('Number of nodes = ', number_of_nodes)
        print('Evaluation = ', final_eval, '\n')
        move = move.bit_length() - 1 # Gets move bit length
        col = move % 8
        row = move // 8
        move = [row, col]
        return jsonify({"move": move})
    else:
        return jsonify({"error": "Invalid request method"})    

def heuristic_evaluation(game_state):
    evaluation = 0  # Positive is good for black
    taken_spaces = game_state.black_bitboard | game_state.white_bitboard
    inverted_bitboard = taken_spaces ^ (1 << 64) - 1 # XOR with board of 1's
    no_empty_spaces = number_of_bits_set(inverted_bitboard)
    corners = [1, 1 << 7, 1 << 56, 1 << 63]
    for corner in corners:
        if game_state.black_bitboard & corner:
            evaluation += 7
        elif game_state.white_bitboard & corner:
            evaluation -= 7

    X_squares = [1 << 9, 1<< 14, 1 << 47, 1 << 54]
    for index in range(4):
        corner = corners[index]
        if taken_spaces & corner:
            # Also checking corner not already filled otherwise no point counting 
            # this X square
            break
        square = X_squares[index]
        if square & game_state.black_bitboard:
            evaluation -= 2
        elif square & game_state.white_bitboard:
            evaluation += 2
    
    if no_empty_spaces > 20:
        game_state.current_player = 1
        no_black_moves = number_of_bits_set(find_legal_moves(game_state))
        evaluation += no_black_moves
        game_state.current_player = 2
        no_white_moves = number_of_bits_set(find_legal_moves(game_state))
        evaluation -= no_white_moves

    elif no_empty_spaces > 10:
        game_state.current_player = 1
        no_black_moves = number_of_bits_set(find_legal_moves(game_state))
        evaluation += no_black_moves
        game_state.current_player = 2
        no_white_moves = number_of_bits_set(find_legal_moves(game_state))
        evaluation -= no_white_moves
        # Next count the pieces of each player for the eval
        evaluation += number_of_bits_set(game_state.black_bitboard)
        evaluation -= number_of_bits_set(game_state.white_bitboard)

    else: # In this case there are <= 10 moves left
        evaluation += number_of_bits_set(game_state.black_bitboard)
        evaluation -= number_of_bits_set(game_state.white_bitboard)
    return evaluation

def number_of_bits_set(bitboard):
    # Don't need to worry about having to copy bitboard since it is immuatble
    # Below makes sure 
    no_bits = 0
    while bitboard:
        no_bits += 1
        bitboard &= (bitboard - 1)
        # The minus 1 above will turn rightmost 1 bit to a 0 and the 
        # zeros to the right of that into ones
    return no_bits

def alpha_beta_move(game_state, depth, alpha, beta):
    # This function just returns the move 
    global number_of_nodes
    number_of_nodes += 1
    
    legal_moves = find_legal_moves(game_state)
    best_move = legal_moves & -legal_moves # Extacts least significant bit
    # ^ Don't have best_move = None to avoid error if position is lost
    # since in that case code below would not return a move
    if game_state.current_player == 1:
        # In this case, we want to maximise the evaluation
        eval = float('-inf')
        while legal_moves:
            move_bitboard = legal_moves & -legal_moves # Extacts least significant bit 
            legal_moves ^= move_bitboard # Gets rid of move just extracted using XOR
            # Make a copy since class instance is mutable
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move_bitboard)
            eval_of_current_move = alpha_beta_evaluation\
                    (new_game_state, depth - 1, alpha, beta)
            if eval_of_current_move > eval:
                best_move = move_bitboard
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
        for move in legal_moves:
            new_board = board.copy()
            new_board, new_player = handle_legal_move(new_board, current_player, move)
            eval_of_current_move = alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta)
            if eval_of_current_move > eval:
                best_move = move
                eval = eval_of_current_move
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return eval, best_move
    else:
        eval = float('inf')
        while legal_moves:
            move_bitboard = legal_moves & -legal_moves # Extacts least significant bit
            legal_moves ^= move_bitboard # Gets rid of move just extracted
            # Make a copy since class instance is mutable
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move_bitboard)
            eval_of_current_move = alpha_beta_evaluation\
                    (new_game_state, depth - 1, alpha, beta)
            if eval_of_current_move < eval:
                best_move = move_bitboard
                eval = eval_of_current_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return eval, best_move
        for move in legal_moves:
            new_board = board.copy()
            new_board, new_player = handle_legal_move(new_board, current_player, move)
            eval_of_current_move = alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta)
            if eval_of_current_move < eval:
                best_move = move
                eval = eval_of_current_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return eval, best_move

def alpha_beta_evaluation(game_state, depth, alpha, beta):
    # This function just returns the eval
    global number_of_nodes
    number_of_nodes += 1
    if depth == 0:
        eval = heuristic_evaluation(game_state)
        return eval

    legal_moves = find_legal_moves(game_state)
    if not legal_moves: # Deal with passing turns here
        game_state.current_player = 1 if game_state.current_player == 2 else 2
        legal_moves = find_legal_moves(game_state)
        if not legal_moves: # In this case, game is over
            # Number black discs minus no white discs
            black_white_difference = number_of_bits_set(game_state.black_bitboard) \
                - number_of_bits_set(game_state.white_bitboard)
            if black_white_difference > 0:
                return float('inf')
            elif black_white_difference < 0:
                return float('-inf')
            else:
                return 0
        # If there are legal moves then the function will continue executing
        # current_player already swapped above
    if game_state.current_player == 1:
        # In this case, we want to maximise the evaluation
        eval = float('-inf')
        while legal_moves:
            move_bitboard = legal_moves & -legal_moves # Extacts least significant bit 
            legal_moves ^= move_bitboard # Gets rid of move just extracted
            # Make a copy since class instance is mutable
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move_bitboard)
            eval = max(eval, alpha_beta_evaluation\
                (new_game_state, depth - 1, alpha, beta))
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return eval
        for move in legal_moves:
            new_board = board.copy()
            new_board, new_player = handle_legal_move(new_board, current_player, move)
            eval = max(eval, alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta))
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return eval
    else:
        eval = float('inf')
        while legal_moves:
            move_bitboard = legal_moves & -legal_moves # Extacts least significant bit 
            legal_moves ^= move_bitboard # Gets rid of move just extracted
            # Make a copy since class instance is mutable
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move_bitboard)
            eval = min(eval, alpha_beta_evaluation\
                (new_game_state, depth - 1, alpha, beta))
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return eval
        for move in legal_moves:
            new_board = board.copy()
            new_board, new_player = handle_legal_move(new_board, current_player, move)
            eval = min(eval, alpha_beta_evaluation\
                (new_board, new_player, depth - 1, alpha, beta))
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return eval
