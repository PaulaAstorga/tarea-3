from players.player import Player
from algorithms.max_n import max_n


class Max3Player(Player):
    def __init__(self, id, view, board_array, eval_function, depth):
        super().__init__(id, view, board_array)
        self.eval_function = eval_function
        self.depth = depth
    

    def get_selected_move(self):
        _, selected_move = max_n(self.board_array, self.id, self.depth,
                                eval_function=self.eval_function, player_amount=3)
        return selected_move