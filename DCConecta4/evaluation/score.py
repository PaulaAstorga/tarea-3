from board.board_helper import BoardHelper

def defensive_simple_score(board, player_id):
    opponent_id = 3 - player_id
    score = 0
    THREE_WEIGHT = 10
    TWO_WEIGHT = 1

    player_fours = BoardHelper.count_consecutive_pieces(board, opponent_id, 4)
    if (player_fours > 0):
        return 1000

    player_threes = BoardHelper.count_consecutive_pieces(board, opponent_id, 3)
    score += player_threes * THREE_WEIGHT

    player_twos = BoardHelper.count_consecutive_pieces(board, opponent_id, 2)
    score += player_twos * TWO_WEIGHT

    return -1 * score

def chat_gpt_eval(board, player: int) -> float:
    opponent = 3 - player
    total_score = 0

    def evaluate_line(line):
        score = 0
        counts = {player: 0, opponent: 0, 0: 0}
        for cell in line:
            counts[cell] += 1

        # Ponderación para el jugador actual
        if counts[player] == 4:
            score += 100000  # victoria
        elif counts[player] == 3 and counts[0] == 1:
            score += 100
        elif counts[player] == 2 and counts[0] == 2:
            score += 10

        # Penalización por amenaza del oponente
        if counts[opponent] == 3 and counts[0] == 1:
            score -= 80
        elif counts[opponent] == 2 and counts[0] == 2:
            score -= 5
        return score

    # Centro del tablero favorece el control
    center_col = [board[row][3] for row in range(6)]
    center_count = center_col.count(player)
    total_score += center_count * 6

    total_rows, total_cols = board.shape

    # Evaluar todas las posibles líneas de 4 celdas
    for row in range(total_rows):
        for col in range(total_cols - 4 + 1):  # horizontal
            line = [board[row][col + i] for i in range(4)]
            total_score += evaluate_line(line)

    for col in range(total_cols):
        for row in range(total_rows - 4 + 1):  # vertical
            line = [board[row + i][col] for i in range(4)]
            total_score += evaluate_line(line)

    for row in range(total_rows - 4 + 1):
        for col in range(total_cols - 4 + 1):
            diag1 = [board[row + i][col + i] for i in range(4)]  # diagonal ↘
            diag2 = [board[row + 3 - i][col + i] for i in range(4)]  # diagonal ↗
            total_score += evaluate_line(diag1)
            total_score += evaluate_line(diag2)

    return total_score

 
#--- AÑADE AQUÍ TUS FUNCIONES DE EVALUACIÓN  ---#