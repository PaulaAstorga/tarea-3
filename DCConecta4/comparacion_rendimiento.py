

from game_controller import GameController
from players import MinimaxPlayer
from view import NoView
from board.board import Board
from evaluation.score import defensive_simple_score, chat_gpt_eval, simple_aggressive_eval

def jugar_partida(depth1, depth2, ia1, ia2):
    board = Board(6, 7)
    board_array = board.get_board_array()
    view = NoView(board)

    player1 = MinimaxPlayer(1, view, board_array, eval_function=ia1, depth=depth1, use_alphabeta=True)
    player2 = MinimaxPlayer(2, view, board_array, eval_function=ia2, depth=depth2, use_alphabeta=True)

    game = GameController([player1, player2], view, board_array)
    game.play(time_execution=True)

    tiempos = game.total_time  # lista de tiempos por jugador
    jugadas = game.total_plays  # lista de jugadas por jugador
    avg_times = {1: tiempos[0] / jugadas[0], 2: tiempos[1] / jugadas[1]}
    return {"ganador": game.winner_id, "tiempo promedio": avg_times}

def promedio(tiempos):
    return round(sum(tiempos) / len(tiempos), 4) if tiempos else 0.0

def simular_configuracion(depth1, depth2,ia1,ia2,repeticiones=10):
    wins = {1: 0, 2: 0, -1: 0}
    tiempos = {1: [], 2: []}

    print(f"Simulando configuración profundidad {depth1} vs {depth2}\n")

    for _ in range(repeticiones):
        resultado = jugar_partida(depth1, depth2,ia1,ia2)
        ganador = resultado["ganador"]
        if ganador is not None:
            wins[ganador] += 1
        tiempos[1].append(resultado["tiempo promedio"][1])
        tiempos[2].append(resultado["tiempo promedio"][2])

    ganador_mas_frecuente = max(wins, key=wins.get)
    if ganador_mas_frecuente == -1:
        resultado_ganador = "Empates predominantes"
    else:
        resultado_ganador = f"Jugador {ganador_mas_frecuente}"

    return f"Ganador más frecuente: {resultado_ganador} - gano {(wins[ganador_mas_frecuente]/10)*100}%" + f" Tiempo promedio J1 (prof {depth1}): {promedio(tiempos[1])}s" +f" Tiempo promedio J2 (prof {depth2}): {promedio(tiempos[2])}s\n" 

if __name__ == "__main__":

    configuraciones = [(1, 1, defensive_simple_score, simple_aggressive_eval), (2, 2, defensive_simple_score, simple_aggressive_eval)]
    text = ""
    for d1, d2, ia1,ia2 in configuraciones:
        text += simular_configuracion(d1, d2, ia1,ia2,repeticiones=10)
    print(text) 
