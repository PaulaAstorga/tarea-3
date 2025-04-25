import copy
from heuristics import nn_policy, manhattan

# NO MODIFICAR

class Puzzle15State:
    def __init__(self, board):
        self.board = board

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        return str(self.board)

    def is_goal(self):
        return self.board == [["1", "2", "3", "4"],
                          ["5", "6", "7", "8"],
                          ["9", "10", "11", "12"],
                          ["13", "14", "15", "X"]]


    def find_X(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == "X":
                    return i, j

    def action_to_index(self, action_str):
        mapping = {
            "left": 0,
            "down": 1,
            "right": 2,
            "up": 3
        }
        return mapping[action_str]


    def h_successors(self, heuristic):
        """
        Genera sucesores junto con el valor de la heurística 'heuristic':
          - Si es nn_policy, 'heuristic(self)' devuelve un vector de 4 probabilidades,
            y usamos cada probabilidad como 'h_nn' para ese movimiento.
          - Si es cualquier otra función, asumimos que devuelve un escalar.
        Retorna lista de tuplas: (nuevo_estado, acción, costo, h_inad)
        """
        actions = [
            ("left",  (0, -1)), 
            ("down",  (1,  0)),
            ("right", (0,  1)), 
            ("up",    (-1, 0))]

        x0, y0 = self.find_X()
        succs = []

        # Si la heurística es la política de la red, obtenemos las probabilidades
        use_policy = (heuristic is nn_policy)
        if use_policy:
            probs = heuristic(self)  # vector de 4 probabilidades

        for idx, (nombre, (dx, dy)) in enumerate(actions):
            # calcular nueva posición del hueco
            nx = x0 + dx
            ny = y0 + dy
            if not (0 <= nx < 4 and 0 <= ny < 4):
                # movimiento inválido: saltamos
                continue

            # swap en una copia del tablero
            nuevo_tablero = copy.deepcopy(self.board)
            nuevo_tablero[x0][y0], nuevo_tablero[nx][ny] = (
                nuevo_tablero[nx][ny],
                nuevo_tablero[x0][y0],
            )
            nuevo_estado = Puzzle15State(nuevo_tablero)

            # 4º valor: heurística inadmisible (scalar o probabilidad)
            if use_policy:
                h_nn = float(probs[idx])   # probabilidad de esa acción
            else:
                h_nn = float(heuristic(nuevo_estado))

            # costo = 1 por cada movimiento
            succs.append((nuevo_estado, nombre, 1, h_nn))

        return succs


class Puzzle15:
    def __init__(self, problem_name):
        self.initial_state = Puzzle15State(self.read_problem(problem_name))

    def read_problem(self, name):
        with open(f"problemas/{name}", "r") as file:
            line = file.readline().strip()
        valores = line.split(" ")
        return [valores[i*4:(i+1)*4] for i in range(4)]

    def heuristic(self, state):
        return Puzzle15.heuristic_static(state)

    def fvalue(self, g, h):
        return g + h
    
