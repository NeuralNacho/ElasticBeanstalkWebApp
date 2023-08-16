import threading
import multiprocessing

class OthelloGameState:
    def __init__(self, black_bitboard, white_bitboard, current_player):
        # Three game state variables:
        self.black_bitboard = black_bitboard
        self.white_bitboard = white_bitboard
        self.current_player = current_player

class OthelloSearchState:
    # Class used to store information about the search for each node
    # in the alpha beta search
    def __init__(self, best_moves, hash_moves, depth, max_depth, alpha = float('-inf'), \
                 beta = float('inf'), node_count = 0):
        self.best_moves = best_moves
        self.hash_moves = hash_moves
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.max_depth = max_depth
        self.node_count = node_count
        # Node count is how many nodes we've checked before this one.
        # Will be used to display the number of nodes checked

def get_game_state(board, current_player):
    black_bitboard, white_bitboard = get_bitboards(board)
    return OthelloGameState(black_bitboard, white_bitboard, current_player)

def get_bitboards(board):
    black_bitboard = 0
    white_bitboard = 0

    for row in range(8):
        for col in range(8):
            index = row * 8 + col
            if board[row][col] == 'black':
                black_bitboard |= 1 << index
            elif board[row][col] == 'white':
                white_bitboard |= 1 << index
    return black_bitboard, white_bitboard

def find_legal_moves(game_state):
    not_left_side = 0xFEFEFEFEFEFEFEFE
    not_right_side = 0x7F7F7F7F7F7F7F7F
    legal_moves_bitboard = 0
    player_bitboard = game_state.black_bitboard if game_state.current_player == 1 \
        else game_state.white_bitboard
    opponent_bitboard = game_state.black_bitboard if game_state.current_player == 2 \
        else game_state.white_bitboard

    def up_left_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        # Get the empty spaces
        checker ^= player_bitboard | opponent_bitboard

        # Get all empty spaces with opponent disc up and left
        # Also make sure discs aren't wrapped around for either player's board
        opponent_bitboard_shifted = not_left_side & (opponent_bitboard << 9)
        player_bitboard_shifted = not_left_side & (player_bitboard << 9)
        checker &= opponent_bitboard_shifted
        while checker:
            # Get some new legal moves
            player_bitboard_shifted = not_left_side & (player_bitboard_shifted << 9)
            legal_moves_bitboard |= checker & (player_bitboard_shifted)
            # Get all empty spaces with a number of opponet discs up and left
            opponent_bitboard_shifted = not_left_side & (opponent_bitboard_shifted << 9)
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def up_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = opponent_bitboard << 8
        player_bitboard_shifted = player_bitboard << 8
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted <<= 8
            legal_moves_bitboard |= checker & player_bitboard_shifted
            opponent_bitboard_shifted <<= 8
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def up_right_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = not_right_side & (opponent_bitboard << 7)
        player_bitboard_shifted = not_right_side & (player_bitboard << 7)
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted = not_right_side & (player_bitboard_shifted << 7)
            legal_moves_bitboard |= checker & (player_bitboard_shifted)
            opponent_bitboard_shifted = not_right_side & (opponent_bitboard_shifted << 7)
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def left_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = not_left_side & (opponent_bitboard << 1)
        player_bitboard_shifted = not_left_side & (player_bitboard << 1)
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted = not_left_side & (player_bitboard_shifted << 1)
            legal_moves_bitboard |= checker & (player_bitboard_shifted)
            opponent_bitboard_shifted = not_left_side & (opponent_bitboard_shifted << 1)
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def right_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = not_right_side & (opponent_bitboard >> 1)
        player_bitboard_shifted = not_right_side & (player_bitboard >> 1)
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted = not_right_side & (player_bitboard_shifted >> 1)
            legal_moves_bitboard |= checker & (player_bitboard_shifted)
            opponent_bitboard_shifted = not_right_side & (opponent_bitboard_shifted >> 1)
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def down_left_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = not_left_side & (opponent_bitboard >> 7)
        player_bitboard_shifted = not_left_side & (player_bitboard >> 7)
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted = not_left_side & (player_bitboard_shifted >> 7)
            legal_moves_bitboard |= checker & (player_bitboard_shifted)
            opponent_bitboard_shifted = not_left_side & (opponent_bitboard_shifted >> 7)
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def down_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = opponent_bitboard >> 8
        player_bitboard_shifted = player_bitboard >> 8
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted >>= 8
            legal_moves_bitboard |= checker & player_bitboard_shifted
            opponent_bitboard_shifted >>= 8
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    def down_right_finder(queue):
        legal_moves_bitboard = 0
        checker = (1 << 64) - 1
        checker ^= player_bitboard | opponent_bitboard
        opponent_bitboard_shifted = not_right_side & (opponent_bitboard >> 9)
        player_bitboard_shifted = not_right_side & (player_bitboard >> 9)
        checker &= opponent_bitboard_shifted
        while checker:
            player_bitboard_shifted = not_right_side & (player_bitboard_shifted >> 9)
            legal_moves_bitboard |= checker & (player_bitboard_shifted)
            opponent_bitboard_shifted = not_right_side & (opponent_bitboard_shifted >> 9)
            checker &= (opponent_bitboard_shifted)
        queue.put(legal_moves_bitboard)
        # return legal_moves_bitboard

    moves_queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target = up_left_finder, args = (moves_queue,))
    p2 = multiprocessing.Process(target = up_finder, args = (moves_queue,))
    p3 = multiprocessing.Process(target = up_right_finder, args = (moves_queue,))
    p4 = multiprocessing.Process(target = left_finder, args = (moves_queue,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    legal_moves_bitboard |= moves_queue.get()
    legal_moves_bitboard |= moves_queue.get()
    legal_moves_bitboard |= moves_queue.get()
    legal_moves_bitboard |= moves_queue.get()

    p1 = multiprocessing.Process(target = right_finder, args = (moves_queue,))
    p2 = multiprocessing.Process(target = down_left_finder, args = (moves_queue,))
    p3 = multiprocessing.Process(target = down_finder, args = (moves_queue,))
    p4 = multiprocessing.Process(target = down_right_finder, args = (moves_queue,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    legal_moves_bitboard |= moves_queue.get()
    legal_moves_bitboard |= moves_queue.get()
    legal_moves_bitboard |= moves_queue.get()
    legal_moves_bitboard |= moves_queue.get()
    # legal_moves_bitboard |= up_left_finder()
    # legal_moves_bitboard |= up_finder()
    # legal_moves_bitboard |= up_right_finder()
    # legal_moves_bitboard |= left_finder()
    # legal_moves_bitboard |= right_finder()
    # legal_moves_bitboard |= down_left_finder()
    # legal_moves_bitboard |= down_finder()
    # legal_moves_bitboard |= down_right_finder()
    return legal_moves_bitboard

def handle_legal_move(game_state, move_bitboard):
    # Add the disc placed to the correct colour's board
    if game_state.current_player == 1:
        game_state.black_bitboard |= move_bitboard
    else:
        game_state.white_bitboard |= move_bitboard

    game_state = flip_discs(game_state, move_bitboard)
    game_state.current_player = 1 if game_state.current_player == 2 else 2
    return game_state

def flip_discs(game_state, move_bitboard):
    not_left_side = 0xFEFEFEFEFEFEFEFE
    not_right_side = 0x7F7F7F7F7F7F7F7F
    player_bitboard = game_state.black_bitboard if game_state.current_player == 1 \
        else game_state.white_bitboard
    opponent_bitboard = game_state.black_bitboard if game_state.current_player == 2 \
        else game_state.white_bitboard
    
    def flip_up_left(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard >> 9
        while opponent_bitboard & index & not_right_side:
            discs_to_flip |= index
            index >>= 9
        # Place on player bitboard and delete disc on opponent bitboard
        if player_bitboard & index & not_right_side:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard

    def flip_up(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard >> 8
        while opponent_bitboard & index:
            discs_to_flip |= index
            index >>= 8
        if player_bitboard & index:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard
    
    def flip_up_right(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard >> 7
        while opponent_bitboard & index & not_left_side:
            discs_to_flip |= index
            index >>= 7
        if player_bitboard & index & not_left_side:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard
    
    def flip_left(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard >> 1
        while opponent_bitboard & index & not_right_side:
            discs_to_flip |= index
            index >>= 1
        if player_bitboard & index & not_right_side:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard

    def flip_right(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard << 1
        while opponent_bitboard & index & not_left_side:
            discs_to_flip |= index
            index <<= 1
        if player_bitboard & index & not_left_side:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard

    def flip_down_left(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard << 7
        while opponent_bitboard & index & not_right_side:
            discs_to_flip |= index
            index <<= 7
        if player_bitboard & index & not_right_side:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard

    def flip_down(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard << 8
        while opponent_bitboard & index:
            discs_to_flip |= index
            index <<= 8
        if player_bitboard & index:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard

    def flip_down_right(player_bitboard, opponent_bitboard):
        discs_to_flip = 0
        index = move_bitboard << 9
        while opponent_bitboard & index & not_left_side:
            discs_to_flip |= index
            index <<= 9
        if player_bitboard & index & not_left_side:
            player_bitboard |= discs_to_flip
            opponent_bitboard &= ~discs_to_flip
        return player_bitboard, opponent_bitboard
    
    player_bitboard, opponent_bitboard = flip_up_left(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_up(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_up_right(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_left(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_right(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_down_left(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_down(player_bitboard, opponent_bitboard)
    player_bitboard, opponent_bitboard = flip_down_right(player_bitboard, opponent_bitboard)

    game_state.black_bitboard = player_bitboard if game_state.current_player == 1\
        else opponent_bitboard
    game_state.white_bitboard = player_bitboard if game_state.current_player == 2\
        else opponent_bitboard
    return game_state

def get_move_index(move):
    # Function to go from move bitboard to row col index
    move = move.bit_length() - 1 # Gets move bit length
    col = move % 8
    row = move // 8
    move = [row, col]
    return move

def print_bitboard(bitboard):
    # Useful for debugging
    for row in range(8):
        row_string = ""
        for col in range(8):
            if bitboard & (1 << row*8 + col):
                row_string += "X "
            else:
                row_string += ". "
        print(row_string)
