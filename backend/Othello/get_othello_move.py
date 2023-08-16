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
        max_depth = 7
        start_time = time.time()
        move, evaluation = iterative_deepening_search(game_state, max_depth)
        cProfile.runctx("iterative_deepening_search(game_state, max_depth)", locals(), globals())
        print('Time = ', time.time() - start_time)
        print('Number of nodes = ', number_of_nodes)
        print('Evaluation = ', evaluation, '\n')
        move = get_move_index(move)
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
    no_bits = 0
    while bitboard:
        no_bits += 1
        bitboard &= (bitboard - 1)
        # The minus 1 above will turn rightmost 1 bit to a 0 and the 
        # zeros to the right of that into ones
    return no_bits

def iterative_deepening_search(game_state, max_depth):
    # Key idea: best_moves and hash_moves are mutable and so every
    # search_state instance is refering to the same dictionaries
    search_state = OthelloSearchState({}, {}, 1, max_depth)
    for depth in range(1, max_depth + 1):
        game_state_copy = OthelloGameState(game_state.black_bitboard, \
                game_state.white_bitboard, game_state.current_player)
        # Need to reset initial alpha and beta of search state for new search
        search_state.depth = depth
        search_state.alpha = float('-inf')
        search_state.beta = float('inf')
        final_evaluation = alpha_beta_search(game_state_copy, search_state)
        # alpha_beta_search will also update best_moves and hash_moves
    game_state_key = (game_state.black_bitboard, game_state.white_bitboard, \
                        game_state.current_player)
    best_move = search_state.best_moves.get(game_state_key)
    return best_move, final_evaluation

def alpha_beta_search(game_state, search_state):
    # Iterate this method but also recursively use
    global number_of_nodes
    number_of_nodes += 1
    if search_state.depth == 0:
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
    
    best_move = legal_moves & -legal_moves # Extacts least significant bit
    # Avoid error if position is lost since in that case code below would not return a move

    legal_moves_in_order = order_legal_moves(legal_moves, game_state, search_state)
    # print([get_move_index(move) for move in legal_moves_in_order])

    if game_state.current_player == 1:
        eval = float('-inf')
        for move in legal_moves_in_order:
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move)
            new_search_state = OthelloSearchState(search_state.best_moves, search_state.hash_moves,\
                    search_state.depth - 1, search_state.max_depth, search_state.alpha, search_state.beta)
            eval_of_current_move = alpha_beta_search(new_game_state, new_search_state)
            if eval_of_current_move > eval:
                best_move = move
                eval = eval_of_current_move
            search_state.alpha = max(search_state.alpha, eval)
            # print('current_player = 1. Alpha = ', search_state.alpha, 'Beta', search_state.beta)
            if search_state.alpha >= search_state.beta:
                add_best_move(game_state, search_state.best_moves, best_move)
                # best_move is also the move which caused the cutoff so is considered for hash_moves
                # Remember best_moves may change so if best_move is added to hash_moves we're not
                # just creating a copy of best_moves
                consider_hash_move(game_state, search_state, best_move)
                # Standard beta cutoff condition where alpha is guarunteed max eval and beta is
                # guarunteed min eval at any given node
                break
        add_best_move(game_state, search_state.best_moves, best_move)
        return eval

    else:
        eval = float('inf')
        for move in legal_moves_in_order:
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move)
            new_search_state = OthelloSearchState(search_state.best_moves, search_state.hash_moves,\
                    search_state.depth - 1, search_state.max_depth, search_state.alpha, search_state.beta)
            eval_of_current_move = alpha_beta_search(new_game_state, new_search_state)
            if eval_of_current_move < eval:
                best_move = move
                eval = eval_of_current_move
            search_state.beta = min(search_state.beta, eval)
            # print('current_player = 2. Alpha = ', search_state.alpha, 'Beta', search_state.beta)
            if search_state.alpha >= search_state.beta:
                add_best_move(game_state, search_state.best_moves, best_move)
                consider_hash_move(game_state, search_state, best_move)
                break
        add_best_move(game_state, search_state.best_moves, best_move)
        return eval

def order_legal_moves(legal_moves_bitboard, game_state, search_state):
    legal_moves = []
    game_state_key = (game_state.black_bitboard, game_state.white_bitboard,\
                        game_state.current_player)
    
    best_move = search_state.best_moves.get(game_state_key, 0)
    if best_move:
        legal_moves += [best_move]
    
    hash_moves_list = search_state.hash_moves.get(game_state_key, [])
    for hash_move in hash_moves_list:
        if not hash_move & best_move:
            legal_moves.insert(1, hash_move)

    while legal_moves_bitboard:
        move_bitboard = legal_moves_bitboard & -legal_moves_bitboard
        legal_moves_bitboard ^= move_bitboard # Delete move off board with XOR
        if move_bitboard & best_move:
            # This move has already been added to the list
            continue
        allow_append = True
        for hash_move in hash_moves_list:
            if move_bitboard & hash_move:
                allow_append = False
                continue
        if allow_append:
            legal_moves.append(move_bitboard)
    
    return legal_moves

def add_best_move(game_state, best_moves_dict, best_move):
    # Use tuple for key since it is immuatable
    game_state_key = (game_state.black_bitboard, game_state.white_bitboard,\
                        game_state.current_player)
    best_moves_dict[game_state_key] = best_move

def consider_hash_move(game_state, search_state, move_considered):
    # Will add hash move depending on if cutoff exceeds threshold
    threshold = 3
    game_state_key = (game_state.black_bitboard, game_state.white_bitboard,\
                        game_state.current_player)
    number_of_layers_cutoff = search_state.max_depth - search_state.depth - 1
    if number_of_layers_cutoff >= threshold:
        hash_moves_list = search_state.hash_moves.get(game_state_key, [])
        for hash_move in hash_moves_list:
            if hash_move & move_considered:
                # Don't want to add duplicate moves
                return
        if hash_moves_list:
            hash_moves_list += [move_considered]
        else:
            search_state.hash_moves[game_state_key] = [move_considered]