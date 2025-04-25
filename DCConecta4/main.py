from game_controller import GameController
from players import MinimaxPlayer, RandomPlayer, HumanPlayer
from view import GraphicView, ConsoleView, NoView
from board.board import Board

### Importar las funciones de evaluación necesarias
from evaluation.score import defensive_simple_score, chat_gpt_eval


board = Board(6, 7)
board_array = board.get_board_array()

###  Elige una view para utilizar: GraphicView, ConsoleView, NoView ###
view = GraphicView(board)


### Inicializa el tipo de jugador: MinimaxPlayer, RandomPlayer, HumanPlayer ###
### MinimaxPlayes(id, view, board_array, eval_function, depth, use_alphabeta)
### RandomPlayer(id, view, board_array)
### HumanPlayer(id, view, board_array)
player1 = MinimaxPlayer(1, view, board_array, eval_function=chat_gpt_eval, depth=1, use_alphabeta=True)
player2 = MinimaxPlayer(2, view, board_array, eval_function=defensive_simple_score, depth=1, use_alphabeta=True)
# player2 = HumanPlayer(2, view, board_array)

### NO MODIFICAR
game = GameController([player1, player2], view, board_array)
game.play(time_execution=True)