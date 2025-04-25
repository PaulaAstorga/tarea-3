from board.board_helper import BoardHelper
import pygame
import time

### NO MODIFICAR

class GameController:
    def __init__(self, players, view, board_array):
        self.board_array = board_array
        self.view = view
        self.winner_id = None
        self.turn_index = 0
        self.players = players
        self.player_amount = len(self.players)
        self.total_time = [0 for _ in range(self.player_amount)]
        self.total_plays = [0 for _ in range(self.player_amount)]


    def play(self, time_execution=False):
        while self.winner_id is None:
            current_player = self.players[self.turn_index]
            
            self.handle_turn(current_player, time_execution)
            self.view.draw_board()
            self.winner_id = self.get_winner_id_or_none()
            self.switch_turn_index()

            #pygame.time.wait(1000) # espera entre turnos
        
        self.view.show_winner(self.winner_id)
        self.print_final_board()

        if time_execution:
            print(f"Tiempos y Cantidad de turnos:")
            
            for i in range(len(self.players)):
                print(f"J{i+1} : {self.total_time[i]:.3f} en total.")
                print(f"   : {(self.total_time[i] / self.total_plays[i]):.3f} en promedio.")
                print(f"   : {self.total_plays[i]} cantidad de turnos jugados")

    
    def handle_turn(self, current_player, time_execution):
        if time_execution:
            start = time.time()

        selected_move = current_player.get_selected_move()

        if time_execution:
            diff = time.time() - start
            self.total_time[self.turn_index] += diff
            self.total_plays[self.turn_index] += 1
            print(f"--> Tiempo de jugada del J{current_player.id}: {diff}s.")
        
        self.execute_move(selected_move, self.board_array, current_player.id)

    
    def switch_turn_index(self):
        self.turn_index = (self.turn_index + 1) % self.player_amount


    def get_winner_id_or_none(self):
        winners = []
        for player in self.players:
            if BoardHelper.has_player_won(self.board_array, player.id):
                winners.append(player.id)
        
        if len(winners) == 1:
            return winners[0]
        
        elif len(winners) > 1: # podrían ganar dos jugadores al mismo tiempo!
            return -1
        
        if BoardHelper.is_board_full(self.board_array):
            return -1



    def execute_move(self, move, board_array, current_player_id):
        BoardHelper.put_piece(board_array, move[0], move[1], current_player_id)
        #self.view.draw_board() # mostrar antes de la rotación
        #pygame.time.wait(500) # espera entre poner la pieza y rotar la columna
        BoardHelper.spin_column(board_array, move[1])


    def print_final_board(self):
        print("========================")
        print("     Tablero final")
        print(self.board_array)
        print("========================")