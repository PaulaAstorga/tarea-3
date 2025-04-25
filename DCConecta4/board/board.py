import numpy as np

class Board:
    def __init__(self, rows_amount, columns_amount):
        self._board = np.zeros((rows_amount, columns_amount))
        self.rows_amount = rows_amount
        self.columns_amount = columns_amount
    
    
    def get_board_array(self):
        return self._board

    
    def is_valid_location(self, row, col):
        return self._board[row, col] == 0


    def print_board(self):
        print(self._board)