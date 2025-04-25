from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def handle_piece_placement(self, player_id):
        pass


    @abstractmethod
    def draw_board(self):
        pass


    @abstractmethod
    def show_winner(self, player_id):
        pass