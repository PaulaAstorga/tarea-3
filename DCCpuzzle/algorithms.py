# src/algorithms.py

import time
from collections import deque

from multi_node import MultiNode
from multi_binary_heap import MultiBinaryHeap
from puzzle import Puzzle15State

class SearchResult:
    # NO MODIFICAR
    def __init__(self, path, expansions, elapsed_ms):
        # path: lista de MultiNode desde inicial hasta meta
        self.path = path
        self.expansions = expansions
        self.elapsed_ms = elapsed_ms

class BaseSearch:
    # NO MODIFICAR
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        raise NotImplementedError

class BFS(BaseSearch):

    def solve(self):
        root = MultiNode(self.problem.initial_state)
        frontier = [root]
        explored = set()
        expansions = 0

        t0 = time.time()
        goal_node = None
        while frontier:
            node = frontier.pop(0)
            if node.state.is_goal():
                goal_node = node
                break
            expansions += 1
            explored.add(node.state)

            # h_successors(heuristic) -> (state, action, cost, h_dummy)
            succ = node.state.h_successors(lambda s: 0)
            for succ_state, action, cost, _ in succ:
                if succ_state in explored:
                    continue
                child = MultiNode(succ_state, parent=node, action=action)
                frontier.append(child)

        elapsed_ms = (time.time() - t0) * 1000

        path = []
        cur = goal_node
        while cur:
            path.append(cur)
            cur = cur.parent
        path.reverse()

        return SearchResult(path, expansions, elapsed_ms)


class DFS(BaseSearch):
    # NO MODIFICAR
    def solve(self):
        root = MultiNode(self.problem.initial_state)
        frontier = [root]
        explored = set()
        expansions = 0

        t0 = time.time()
        goal_node = None
        while frontier:
            node = frontier.pop()
            if node.state.is_goal():
                goal_node = node
                break
            expansions += 1
            explored.add(node.state)

            # h_successors(heuristic) -> (state, action, cost, h_dummy)
            succ = node.state.h_successors(lambda s: 0)
            for succ_state, action, cost, _ in succ:
                if succ_state in explored:
                    continue
                child = MultiNode(succ_state, parent=node, action=action)
                frontier.append(child)

        elapsed = (time.time() - t0) * 1000

        path = []
        cur = goal_node
        while cur:
            path.append(cur)
            cur = cur.parent
        path.reverse()
        return SearchResult(path, expansions, elapsed)

class AStar(BaseSearch):
    # Completar - Parte 2
    def __init__(self, problem, heuristic):
        super().__init__(problem)
        self.heuristic = heuristic
        # usaremos heap id=0 para f-values
        self.heap = MultiBinaryHeap(id=0) # puedes cambiarlo a la EDD que prefieras

    def solve(self):
        # nodo raíz
        root = MultiNode(self.problem.initial_state)
        root.g = 0
        root.h[0] = self.heuristic(root.state)
        root.key[0] = root.g + root.h[0]

        # inicializar heap
        self.heap.clear()
        self.heap.insert(root)

        # inicializar contadores y estructuras
        generated = {}
        expansions = 0
        t0 = time.time()
        goal_node = None
        
        while not self.heap.is_empty():
            # Completar - Parte 2
            child = self.heap.extract()

            if child.state.is_goal():
                goal_node = child
                break
            succ = child.state.h_successors(heuristic=self.heuristic)
            expansions += 1

            for child_state, action, cost, h_value in succ:
                child_node = generated.get(child_state)
                is_new = child_node is None  
                path_cost = child.g + cost 

                if is_new or path_cost < child_node.g: #si es visto por 1ra vez o si es un mejor camino se agrega a open.

                    if is_new: 
                        child_node = MultiNode(child_state, child, action)
                        child_node.h[0] = h_value
                        generated[child_state] = child_node

                    child_node.action = action
                    child_node.g = path_cost
                    child_node.key[0] = child_node.g + child_node.h[0]
                    self.heap.insert(child_node) # inserta child_node a la open si no esta en la open
    
        elapsed= (time.time() - t0) * 1000
        # reconstruir camino
        path = []
        cur = goal_node
        while cur:
            path.append(cur)
            cur = cur.parent
        path.reverse()
        return SearchResult(path, expansions, elapsed)