from players.player import Player


class HumanPlayer(Player):
    def __init__(self, id, view, board_array):
        super().__init__(id, view, board_array)


    def get_selected_move(self):
        return self.view.handle_piece_placement(self.id)