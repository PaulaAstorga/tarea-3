import numpy as np
import tensorflow as tf
import os
from litemodel import LiteModel, from_file, from_keras_model
from math import sqrt

# NO MODIFICAR
_model_nn = None
_model_input_idx = None
_model_output_idx = None
_model_input_dtype = None

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def get_heuristic(heuristic):
    if heuristic == "manhattan":
        return manhattan
    elif heuristic == "euclidian":
        return euclidian
    elif heuristic == "smart_heuristic":
        return smart_heuristic
    elif heuristic == "corner_boost":
        return corner_boost
    elif heuristic == "nn":
        _load_nn_model()
        return nn_policy
    # elif heuristic == "": Acá pueden colocar alguna heurística implementada por ustedes
    #     return _
    elif heuristic == "zero":
        return lambda s: 0
    else:
        raise ValueError(f"Heurística desconocida: {heuristic}")

def _load_nn_model():
    # NO MODIFICAR
    global _model_nn, _model_input_idx, _model_output_idx, _model_input_dtype
    if _model_nn is None:
        _model_nn = from_keras_model("15puzzle_solver_model.h5")
        interp = _model_nn.interpreter
        inp_det = interp.get_input_details()[0]
        out_det = interp.get_output_details()[0]
        _model_input_idx  = inp_det["index"]
        _model_input_dtype= inp_det["dtype"]
        _model_output_idx = out_det["index"]
    
def nn_policy(state):
    # NO MODIFICAR
    one_hot_bits = []
    for row in state.board:
        for val in row:
            n = 0 if val == "X" else int(val)
            vec = [0]*16
            vec[n] = 1
            one_hot_bits.extend(vec)

    arr = np.array([one_hot_bits], dtype=_model_input_dtype)

    interp = _model_nn.interpreter
    interp.set_tensor(_model_input_idx, arr)
    interp.invoke()
    out = interp.get_tensor(_model_output_idx)[0]
    # asume que out.sum()==1
    return out

def manhattan(state):
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2),
        "X": (3, 3) 
    }
    dist = 0
    for i in range(4):
        for j in range(4):
            val = state.board[i][j]
            gx, gy = objetivo[val]
            dist += abs(i - gx) + abs(j - gy)
    return dist

def euclidian(state):
    # Completar - Parte 2
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2),
        "X": (3, 3) 
    }
    dist = 0
    for i in range(4):
        for j in range(4):
            val = state.board[i][j]
            gx, gy = objetivo[val]
            dist += sqrt((i - gx)**2 + (j - gy)**2)
            
    return dist


def smart_heuristic(state):
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2),
        "X": (3, 3) 
    }
    dist = 0

    # distancia euclidiana
    for i in range(4):
        for j in range(4):
            val = state.board[i][j]
            if val == "X":
                continue
            gx, gy = objetivo[val]
            dist += sqrt((i - gx)**2 + (j - gy)**2)

    # conflictos lineales en filas
    for fila in range(4):
        for col1 in range(4):
            for col2 in range(col1 + 1, 4):
                val1 = state.board[fila][col1]
                val2 = state.board[fila][col2]
                if val1 == "X" or val2 == "X":
                    continue
                gx1, _ = objetivo[val1]
                gx2, _ = objetivo[val2]
                if gx1 == fila and gx2 == fila and int(val1) > int(val2):
                    dist += 2

    # conflictos lineales en columnas
    for col in range(4):
        for fila1 in range(4):
            for fila2 in range(fila1 + 1, 4):
                val1 = state.board[fila1][col]
                val2 = state.board[fila2][col]
                if val1 == "X" or val2 == "X":
                    continue
                _, gy1 = objetivo[val1]
                _, gy2 = objetivo[val2]
                if gy1 == col and gy2 == col and int(val1) > int(val2):
                    dist += 2

    return dist

# aquí creamos la heurísitica no admisible.
def corner_boost(state):
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2), "X": (3, 3)
    }

    dist = 0
    recompensa = 0

    esquinas = {
        "1": (0, 0),
        "4": (0, 3),
        "13": (3, 0),
        "15": (3, 2)
    }

    for i in range(4):
        for j in range(4):
            val = state.board[i][j]
            gx, gy = objetivo[val]
            dist += sqrt((i - gx)**2 + (j - gy)**2)

            # bonificación si una ficha de esquina está bien posicionada
            if val in esquinas and (i, j) == esquinas[val]:
                recompensa += 1.5  # aumenta el incentivo por esquina bien puesta

    return dist - recompensa