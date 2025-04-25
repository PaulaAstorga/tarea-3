from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, id, view, board_array):
        self.id = id
        self.view = view
        self.board_array = board_array


    @abstractmethod
    def get_selected_move(self):
        # Metodo que obtiene la jugada
        pass