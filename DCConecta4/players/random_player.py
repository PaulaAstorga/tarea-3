from players.player import Player
from random import choice
from board.board_helper import BoardHelper


class RandomPlayer(Player):
    def __init__(self, id, view, board_array):
        super().__init__(id, view, board_array)
    

    def get_selected_move(self):
        return BoardHelper.get_available_cells()