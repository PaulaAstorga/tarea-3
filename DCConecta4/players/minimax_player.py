from players.player import Player
from algorithms.minimax import minimax


class MinimaxPlayer(Player):
    def __init__(self, id, view, board_array, eval_function, depth, use_alphabeta):
        super().__init__(id, view, board_array)
        self.eval_function = eval_function
        self.depth = depth
        self.use_alphabeta = use_alphabeta

    
    def get_selected_move(self):
        _, selected_move = minimax(self.board_array, self.id, fixed_player_id=self.id, depth=self.depth,
                                max_player=True, use_alphabeta=self.use_alphabeta, eval_function=self.eval_function)
        return selected_move
