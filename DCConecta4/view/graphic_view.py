import pygame
import math
from view.view import View


class GraphicView(View):
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)

    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)      # J1
    YELLOW = (255, 255, 0) # J2
    GREEN = (0, 255, 0)    # J3
    
    
    def __init__(self, board):
        self.board = board
        self.color_by_id = {
            1: self.RED,
            2: self.YELLOW,
            3: self.GREEN    
        }
        self.width = board.columns_amount * self.SQUARESIZE
        self.height = board.rows_amount * self.SQUARESIZE
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 50)
        self.previous_row = self.previous_col = None
        self.draw_board()


    def handle_piece_placement(self, player_id):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()

                if event.type == pygame.MOUSEMOTION:
                    self.draw_mouse_motion(*event.pos, player_id)

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col, row = self.get_selected_position(*event.pos)

                    if self.board.is_valid_location(row, col):
                        return row, col



    def draw_board(self):
        rows = self.board.rows_amount
        columns = self.board.columns_amount
        for c in range(columns):
            for r in range(rows):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        board_array = self.board.get_board_array()
        for c in range(columns):
            for r in range(rows):
                if (board_array[r, c] != 0):
                    self.draw_piece(board_array[r, c], r, c)
        
        pygame.display.update()


    def draw_mouse_motion(self, posx, posy, player_id):
        player_color = self.color_by_id[player_id]
        col, row = self.get_selected_position(posx, posy)
        
        if row != self.previous_row or col != self.previous_col:
            self.draw_board()
            self.previous_row = row
            self.previous_col = col

        x_coord, y_coord = self.get_coordinates_to_draw(row, col)
        pygame.draw.circle(self.screen, player_color, (x_coord, y_coord), self.RADIUS)
        pygame.display.update()



    def get_coordinates_to_draw(self, row, col):
        return int(self.SQUARESIZE*(col+0.5)), int(self.SQUARESIZE*(row+0.5))



    def get_selected_position(self, posx, posy):
        return math.floor(posx / self.SQUARESIZE), math.floor(posy / self.SQUARESIZE)


    def draw_piece(self, player_id, row, column):
        color = self.color_by_id[player_id]
        x_coord, y_coord = self.get_coordinates_to_draw(row, column)
        pygame.draw.circle(self.screen, color, (x_coord, y_coord), self.RADIUS)
    

    def show_winner(self, player_id):
        if player_id == -1:
            label = self.font.render("¡Empate!", True, self.BLUE)
            print("¡Empate!")
        else:
            color = self.color_by_id[player_id]
            label = self.font.render(f"¡Ganó el jugador {player_id}!", True, color)
            print(f"¡Ganó el jugador {player_id}!")
        
        self.screen.blit(label, (40, 10))