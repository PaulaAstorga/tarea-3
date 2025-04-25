from tabulate import tabulate

def print_path(node):
    # NO MODIFICAR
    # Dibuja paso a paso el tablero de la solución.
    path = node.path()

    for i, n in enumerate(path):
        print(f"\n🧩 Paso {i}")
        print(tabulate(n.state.board, tablefmt="fancy_grid", colalign=("right",)*4))
        input()

def print_summary(results):
    # NO MODIFICAR
    """
    results: lista de tuplas (alg_name, SearchResult)
    Imprime una tabla con columna:
    [Algoritmo | Longitud | Expansiones | Tiempo (ms)]
    """
    headers = ["Algoritmo", "Longitud", "Expansiones", "Tiempo (s)"]
    table = []
    for name, res in results:
        # res es un SearchResult
        length = len(res.path)-1 if res.path else 0
        table.append([name, length, res.expansions, f"{res.elapsed_ms / 1000:.1f}"])
    print(tabulate(table, headers, tablefmt="fancy_grid"))