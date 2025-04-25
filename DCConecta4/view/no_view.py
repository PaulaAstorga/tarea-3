from view.view import View

class NoView(View):
    def __init__(self, board):
        super().__init__(board)

    def draw_board(self):
        pass
    

    def handle_piece_placement(self, player_id):
        while True:
            row = int(input("Selecciona una fila: "))
            col = int(input("Selecciona una columna: "))

            if self.board.is_valid_location(row, col):
                return row, col
            print("Ubicación inválida. Inténtalo de nuevo.")
    

    def show_winner(self, player_id):
        if player_id == -1:
            print("Empate.")
        else:
            print(f"Ganador: J{player_id}.")