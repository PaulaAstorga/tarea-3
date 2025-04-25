
def fight_against_third(board_array):
    board = board_array  # matriz 6x7
    scores = [0.0, 0.0, 0.0]  # índice 0 → jugador 1, 1 → jugador 2, 2 → jugador 3

    total_row, total_col = board.shape

    def evaluate_line(line):
        counts = {1: 0, 2: 0, 3: 0, 0: 0}
        for cell in line:
            counts[cell] += 1

        for player in [1, 2, 3]:
            idx = player - 1

            # Victoria inmediata
            if counts[player] == 4:
                scores[idx] += 100000
            elif counts[player] == 3 and counts[0] == 1:
                scores[idx] += 100
            elif counts[player] == 2 and counts[0] == 2:
                scores[idx] += 10

        # Si el jugador 3 está cerca de alinear, penalizar eso para jugadores 1 y 2
        if counts[3] == 3 and counts[0] == 1:
            scores[2] += 100  # jugador 3 se acerca a ganar
            scores[0] -= 50   # jugador 1 pierde valor
            scores[1] -= 50   # jugador 2 pierde valor

        elif counts[3] == 2 and counts[0] == 2:
            scores[2] += 10
            scores[0] -= 5
            scores[1] -= 5

        # Bonus si 1 o 2 bloquean activamente a 3
        if counts[3] == 2 and counts[0] == 1 and (counts[1] == 1 or counts[2] == 1):
            if counts[1] == 1:
                scores[0] += 20  # jugador 1 bloqueó a 3
            if counts[2] == 1:
                scores[1] += 20  # jugador 2 bloqueó a 3

    # Evaluar todas las líneas posibles (horizontal, vertical y diagonales)
    for row in range(total_row):
        for col in range(total_col - 3):
            line = [board[row][col + i] for i in range(4)]
            evaluate_line(line)

    for col in range(total_col):
        for row in range(total_row - 3):
            line = [board[row + i][col] for i in range(4)]
            evaluate_line(line)

    for row in range(total_row - 3):
        for col in range(total_col - 3):
            diag1 = [board[row + i][col + i] for i in range(4)]  # \
            diag2 = [board[row + 3 - i][col + i] for i in range(4)]  # /
            evaluate_line(diag1)
            evaluate_line(diag2)

    return tuple(scores)



def chat_gpt_eval_3(board_array):
    board = board_array  # matriz de 6x7
    scores = [0.0, 0.0, 0.0]

    def check_line(line):
        counts = [0, 0, 0, 0]
        for cell in line:
            cell = int(cell)
            counts[cell] += 1
        for player in [1, 2, 3]:
            # victoria
            if counts[player] == 4:
                scores[player-1] += 1000

            # 3 en línea con una celda vacía
            elif counts[player] == 3 and counts[0] == 1:
                scores[player-1] += 5
            # 2 en línea con 2 vacías
            elif counts[player] == 2 and counts[0] == 2:
                scores[player-1] += 2

    total_row, total_col = board.shape
    
    # revisar filas, columnas y diagonales
    for row in range(total_row):
        for col in range(total_col - 3):  # filas horizontales
            check_line([board[row][col + i] for i in range(4)])
    for col in range(total_col):
        for row in range(total_row - 3):  # columnas verticales
            check_line([board[row + i][col] for i in range(4)])
    for row in range(total_row - 3):
        for col in range(total_col - 3):
            # diagonal \
            check_line([board[row + i][col + i] for i in range(4)])
            # diagonal /
            check_line([board[row + 3 - i][col + i] for i in range(4)])

    return scores


#--- AÑADE AQUÍ TUS FUNCIONES DE EVALUACIÓN PARA EL BONUS ---#