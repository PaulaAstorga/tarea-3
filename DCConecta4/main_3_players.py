from game_controller import GameController
from players import Max3Player, RandomPlayer, HumanPlayer
from view import GraphicView, ConsoleView, NoView
from board.board import Board

### Importar las funciones de evaluación necesarias
from evaluation.score_3 import chat_gpt_eval_3, fight_against_third


board = Board(5, 6)
board_array = board.get_board_array()


###  Elige una view para utilizar: GraphicView, ConsoleView, NoView ###
view = GraphicView(board)


### Inicializa el tipo de jugador: Max3Player, RandomPlayer, HumanPlayer ###
player1 = Max3Player(1, view, board_array, chat_gpt_eval_3, 1)
player2 = Max3Player(2, view, board_array, chat_gpt_eval_3, 1)
player3 = Max3Player(3, view, board_array, chat_gpt_eval_3, 3)


game = GameController([player1, player2, player3], view, board_array)
game.play(time_execution=True)