import numpy as np
from random import shuffle

### NO MODIFICAR

class BoardHelper:
    @staticmethod
    def put_piece(board, row, col, piece):
        board[row, col] = piece


    @staticmethod
    def spin_column(board, col):
        board[:, col] = board[::-1, col]


    @staticmethod
    def has_player_won(board_array, piece):
        return BoardHelper.count_consecutive_pieces(board_array, piece, 4) > 0
                

    @staticmethod
    def is_terminal_state(board_array, possible_players):
        for player in possible_players:
            if BoardHelper.has_player_won(board_array, player):
                return True
        return BoardHelper.is_board_full(board_array)
    
    
    @staticmethod
    def is_board_full(board_array):
        return board_array.all()


    def get_available_cells(board):
        rows, cols = np.where(board == 0)
        cells = list(zip(rows, cols))
        shuffle(cells) # para añadir aleatoriedad en cada juego
    
        for cell in cells:
            yield cell

    @staticmethod
    def get_possible_next_states(board, piece):
        for row, column in BoardHelper.get_available_cells(board):
            board_copy = board.copy()
            BoardHelper.put_piece(board_copy, row, column, piece)
            BoardHelper.spin_column(board_copy, column)
            yield (row, column), board_copy

    
    @staticmethod
    def count_consecutive_pieces(board, player_id, consecutive):
        count = 0
        rows, cols = board.shape
        
        # Horizontal
        for row in range(rows):
            for col in range(cols - consecutive + 1):
                if all(board[row, col + i] == player_id for i in range(consecutive)):
                    count += 1
        
        # Vertical
        for row in range(rows - consecutive + 1):
            for col in range(cols):
                if all(board[row + i, col] == player_id for i in range(consecutive)):
                    count += 1
        
        # Diagonal (\) 
        for row in range(rows - consecutive + 1):
            for col in range(cols - consecutive + 1):
                if all(board[row + i, col + i] == player_id for i in range(consecutive)):
                    count += 1
        
        # Diagonal (/)
        for row in range(consecutive - 1, rows):
            for col in range(cols - consecutive + 1):
                if all(board[row - i, col + i] == player_id for i in range(consecutive)):
                    count += 1
        
        return count