class OthelloGame:
    def __init__(self, board, current_player, turns_passed = 0):
        # Three game state variables:
        self.board = board
        self.current_player = current_player
        self.turns_passed = turns_passed

    def create_new_game(self):
        board = [['' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'white'
        self.board[4][4] = 'white'
        self.board[3][4] = 'black'
        self.board[4][3] = 'black'

        self.board = board
        self.current_player = 'black'
        self.turns_passed = 0
    
    def is_valid_move(self, index):
        if self.board[index[0]][index[1]] != '':
            return False
        directions = [[-1, -1], [-1, 0], [-1, 1],
                      [0, -1],           [0, 1],
                      [1, -1],  [1, 0],  [1, 1] ]
        for direction in directions:
            row = index[0] + direction[0]
            col = index[1] + direction[1]
            found_opponent_piece = False
            while row >= 0 and row < 8 and col >= 0 and col < 8:
                if self.board[row][col] == '':
                    break
                if self.board[row][col] != self.current_player:
                    found_opponent_piece = True
                    row += direction[0]
                    col += direction[1]
                    continue
                if found_opponent_piece: 
                    # Must have also met a disc of current player
                    return True
                else:
                    # Have found disc of current player without 
                    # finding opponent piece
                    break

    def find_legal_moves(self):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == '' and self.is_valid_move([row, col]):
                    legal_moves.append([row, col])
        return legal_moves
    
    def handle_legal_move(self, move_index):
        # Update game_state after a move is made
        self.board[move_index[0]][move_index[1]] = self.current_player
        self.flip_discs(move_index)

        if self.current_player == 'black':
            self.current_player = 'white'
        else: self.current_player = 'black'

        self.turns_passed = 0
    
    def flip_discs(self, move_index):
        directions = [[-1, -1], [-1, 0], [-1, 1],
                      [0, -1],           [0, 1],
                      [1, -1],  [1, 0],  [1, 1] ]
        for direction in directions:
            discs_to_flip = []
            row = move_index[0] + direction[0]
            col = move_index[1] + direction[1]
            while row >= 0 and row < 8 and col >= 0 and col < 8:
                if self.board[row][col] == '':
                    break
                if self.board[row][col] != self.current_player:
                    discs_to_flip.append([row, col])
                    row += direction[0]
                    col += direction[1]
                    continue
                if self.board[row][col] == self.current_player:
                    for disc in discs_to_flip:
                        self.board[disc[0]][disc[1]] = self.current_player
                    break