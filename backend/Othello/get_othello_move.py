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
        # cProfile.runctx("iterative_deepening_search(game_state, max_depth)", locals(), globals())
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
            evaluation += 4
        elif game_state.white_bitboard & corner:
            evaluation -= 4

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
    
    C_squares = [1 << 1, 1 << 8, 1 << 6, 1 << 15, 1 << 48, 1 << 57, 1 << 55, 1 << 62]
    C_square_adjacents = [1 << 2, 1 << 16, 1 << 5, 1 << 22, 1 << 40, 1 << 58, 1 << 47, 1 << 61]
    for index, c_sqaure in enumerate(C_squares):
        if not taken_spaces & c_sqaure:
            continue
        
        if index == 0 and not taken_spaces & corners[0]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[0] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[0] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 1 and not taken_spaces & corners[0]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[0] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[0] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 2 and not taken_spaces & corners[1]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[1] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[1] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 3 and not taken_spaces & corners[1]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[1] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[1] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 4 and not taken_spaces & corners[2]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[2] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[2] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 5 and not taken_spaces & corners[2]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[2] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[2] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 6 and not taken_spaces & corners[3]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[3] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[3] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2
        elif index == 7 and not taken_spaces & corners[3]:
            if c_sqaure & game_state.black_bitboard and not \
                X_squares[3] & game_state.black_bitboard and not \
                C_square_adjacents[index] & game_state.black_bitboard:
                evaluation -= 2
            elif c_sqaure & game_state.white_bitboard and not \
                X_squares[3] & game_state.white_bitboard and not \
                C_square_adjacents[index] & game_state.white_bitboard:
                evaluation += 2

    top_row = 0xFF00000000000000
    bottom_row = 0x00000000000000FF
    left_row = 0x8080808080808080
    right_row = 0x0101010101010101
    if not (taken_spaces ^ top_row) & top_row: # i.e. top_row completely filled
        evaluation += number_of_bits_set(game_state.black_bitboard & top_row)
        evaluation -= number_of_bits_set(game_state.white_bitboard & top_row)
    if not (taken_spaces ^ bottom_row) & bottom_row:
        evaluation += number_of_bits_set(game_state.black_bitboard & bottom_row)
        evaluation -= number_of_bits_set(game_state.white_bitboard & bottom_row)
    if not (taken_spaces ^ left_row) & left_row:
        evaluation += number_of_bits_set(game_state.black_bitboard & left_row)
        evaluation -= number_of_bits_set(game_state.white_bitboard & left_row)
    if not (taken_spaces ^ right_row) & right_row:
        evaluation += number_of_bits_set(game_state.black_bitboard & right_row)
        evaluation -= number_of_bits_set(game_state.white_bitboard & right_row)
    for i in range(8):
        square = 1 << i
        if not game_state.black_bitboard & square:
            evaluation += i # Will get extra 2 for any corner! (+1 from each direction)
            # Notice nothing will be added if full row is black since this is
            # already covered in code above
            break
    for i in range(8):
        square = 1 << i
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (7 - i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (7 - i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (56 + i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (56 + i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (63 - i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (63 - i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (8*i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (8*i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (56 - 8*i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (56 - 8*i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (7 + 8*i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (7 + 8*i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break
    for i in range(8):
        square = 1 << (63 - 8*i)
        if not game_state.black_bitboard & square:
            evaluation += i
            break
    for i in range(8):
        square = 1 << (63 - 8*i)
        if not game_state.white_bitboard & square:
            evaluation -= i
            break


    if no_empty_spaces > 18:
        game_state.current_player = 1
        no_black_moves = number_of_bits_set(find_legal_moves(game_state))
        evaluation += no_black_moves
        game_state.current_player = 2
        no_white_moves = number_of_bits_set(find_legal_moves(game_state))
        evaluation -= no_white_moves

    elif no_empty_spaces > 7:
        game_state.current_player = 1
        no_black_moves = 2*number_of_bits_set(find_legal_moves(game_state))
        # 2* so not left without moves late on
        evaluation += no_black_moves
        game_state.current_player = 2
        no_white_moves = 2*number_of_bits_set(find_legal_moves(game_state))
        evaluation -= no_white_moves
        # Next count the pieces of each player for the eval
        evaluation += 0.5*number_of_bits_set(game_state.black_bitboard)
        # 0.5 since are a lot more discs than moves so want to weight appropriately
        evaluation -= 0.5*number_of_bits_set(game_state.white_bitboard)

    else: # In this case there are <= 4 moves left
        evaluation = 0.5*number_of_bits_set(game_state.black_bitboard)
        evaluation -= 0.5*number_of_bits_set(game_state.white_bitboard)
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
    time_taken = 0
    time_up = False
    for depth in range(1, max_depth + 1):
        start_time = time.time()
        game_state_copy = OthelloGameState(game_state.black_bitboard, \
                game_state.white_bitboard, game_state.current_player)
        # Need to reset initial alpha and beta of search state for new search
        search_state.depth = depth
        search_state.alpha = float('-inf')
        search_state.beta = float('inf')
        final_evaluation = alpha_beta_search(game_state_copy, search_state)
        # alpha_beta_search will also update best_moves and hash_moves
        time_taken += time.time() - start_time
        if time_taken > 0.25 and depth > 1:
            print('Max depth achieved 1', depth)
            time_up = True
            break

    increased_depth = 0
    while not time_up and max_depth + increased_depth < 20: 
        # Increase depth if not much time has elapsed
        # Second condition for at game end when don't want to loop excessively
        increased_depth += 1
        if time_taken < 0.25:
            start_time = time.time()
            game_state_copy = OthelloGameState(game_state.black_bitboard, \
                game_state.white_bitboard, game_state.current_player)
            search_state.depth = max_depth + increased_depth
            search_state.alpha = float('-inf')
            search_state.beta = float('inf')
            final_evaluation = alpha_beta_search(game_state_copy, search_state)
            time_taken += time.time() - start_time
        else:
            print('Max depth achieved 2', max_depth + increased_depth - 1)
            break
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
            no_black_discs = number_of_bits_set(game_state.black_bitboard)
            no_white_discs = number_of_bits_set(game_state.white_bitboard)
            black_white_difference = no_black_discs - no_white_discs
            if black_white_difference > 0:
                # Could return +inf but instead do a large number so program will
                # try to win by largest possible margin
                return 100 + black_white_difference
            elif black_white_difference < 0:
                return -100 + black_white_difference
            else:
                return 0
        # If there are legal moves then the function will continue executing
        # current_player already swapped above  
    
    best_move = legal_moves & -legal_moves # Extacts least significant bit
    # Avoid error if position is lost since in that case code below would not return a move

    legal_moves_in_order, number_not_to_reduce = order_legal_moves(legal_moves, game_state, search_state)

    if game_state.current_player == 1:
        eval = float('-inf')
        for index, move in enumerate(legal_moves_in_order):
            # Check if is late move and how much to reduce search by accordingly
            extra_depth_to_reduce = 0
            if index >= number_not_to_reduce and search_state.depth > 2:
                # Dont reduce best or hash moves. Also don't reduce for depth 1 especially
                # because don't want to reduce on first iterative deepening iteration.
                if search_state.max_depth - search_state.depth <= 3:
                    # Don't reduce too much for first few moves
                    extra_depth_to_reduce = 1
                else:
                    extra_depth_to_reduce = int(search_state.depth / 3)
                    if number_not_to_reduce >= 2: 
                        # Previous iteration has cut this node out in this case
                        extra_depth_to_reduce += 1
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move)
            new_search_state = OthelloSearchState(search_state.best_moves, \
                    search_state.hash_moves, search_state.depth - 1 - extra_depth_to_reduce, \
                    search_state.max_depth, search_state.alpha, search_state.beta)
            eval_of_current_move = alpha_beta_search(new_game_state, new_search_state)
            if eval_of_current_move >= search_state.alpha - 1 and extra_depth_to_reduce != 0:
                # Must redo full search in this case (LMR was not correct here)
                new_search_state = OthelloSearchState(search_state.best_moves, \
                    search_state.hash_moves, search_state.depth - 1, \
                    search_state.max_depth, search_state.alpha, search_state.beta)
                eval_of_current_move = alpha_beta_search(new_game_state, new_search_state)
            if eval_of_current_move > eval:
                best_move = move
                eval = eval_of_current_move
            search_state.alpha = max(search_state.alpha, eval)
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
        for index, move in enumerate(legal_moves_in_order):
            extra_depth_to_reduce = 0
            if index >= number_not_to_reduce and search_state.depth > 2:
                if search_state.max_depth - search_state.depth <= 3:
                    extra_depth_to_reduce = 1
                else:
                    extra_depth_to_reduce = int(search_state.depth / 3)
                    if number_not_to_reduce >= 2: 
                        extra_depth_to_reduce += 1
            new_game_state = OthelloGameState(game_state.black_bitboard, \
                        game_state.white_bitboard, game_state.current_player)
            new_game_state = handle_legal_move(new_game_state, move)
            new_search_state = OthelloSearchState(search_state.best_moves, \
                    search_state.hash_moves, search_state.depth - 1 - extra_depth_to_reduce, \
                    search_state.max_depth, search_state.alpha, search_state.beta)
            eval_of_current_move = alpha_beta_search(new_game_state, new_search_state)
            if eval_of_current_move <= search_state.beta + 1 and extra_depth_to_reduce != 0:
                new_search_state = OthelloSearchState(search_state.best_moves, \
                    search_state.hash_moves, search_state.depth - 1, \
                    search_state.max_depth, search_state.alpha, search_state.beta)
                eval_of_current_move = alpha_beta_search(new_game_state, new_search_state)
            if eval_of_current_move < eval:
                best_move = move
                eval = eval_of_current_move
            search_state.beta = min(search_state.beta, eval)
            if search_state.alpha >= search_state.beta:
                add_best_move(game_state, search_state.best_moves, best_move)
                consider_hash_move(game_state, search_state, best_move)
                break
        add_best_move(game_state, search_state.best_moves, best_move)
        return eval

def order_legal_moves(legal_moves_bitboard, game_state, search_state):
    legal_moves = []
    number_of_best_or_hash_moves = 0 # Used for late move reduction
    game_state_key = (game_state.black_bitboard, game_state.white_bitboard,\
                        game_state.current_player)
    
    best_move = search_state.best_moves.get(game_state_key, 0)
    if best_move:
        legal_moves += [best_move]
        number_of_best_or_hash_moves += 1
    
    hash_moves_list = search_state.hash_moves.get(game_state_key, [])
    for hash_move in hash_moves_list:
        if not hash_move & best_move:
            legal_moves.insert(1, hash_move)
            number_of_best_or_hash_moves += 1

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
    
    return legal_moves, number_of_best_or_hash_moves

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