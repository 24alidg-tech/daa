# Hamiltonian Cycle using Backtracking

def is_safe(v, graph, path, pos):
    # Check if this vertex is adjacent to the previous vertex in the path
    if graph[path[pos - 1]][v] == 0:
        return False

    # Check if vertex has already been included
    if v in path:
        return False

    return True


def hamiltonian_cycle_util(graph, path, pos):
    # Base Case: all vertices are included in the path
    if pos == len(graph):
        # Check if last vertex connects to the first vertex
        return graph[path[pos - 1]][path[0]] == 1

    # Try different vertices as the next candidate
    for v in range(1, len(graph)):
        if is_safe(v, graph, path, pos):
            path[pos] = v

            if hamiltonian_cycle_util(graph, path, pos + 1):
                return True

            # Backtrack
            path[pos] = -1

    return False


def hamiltonian_cycle(graph, labels):
    n = len(graph)
    path = [-1] * n
    path[0] = 0  # Start from vertex 0 (Headquarters)

    if not hamiltonian_cycle_util(graph, path, 1):
        print("No Hamiltonian Cycle exists.")
        return

    # Print the cycle using labels
    cycle = [labels[v] for v in path] + [labels[path[0]]]
    print("Hamiltonian Cycle Found:")
    print(" → ".join(cycle))


# ---------- Example 1 ----------
graph1 = [
    [0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0]
]
labels1 = ['A', 'B', 'C', 'D', 'E']

print("Example 1:")
hamiltonian_cycle(graph1, labels1)
print("\n")

# ---------- Example 2 ----------
graph2 = [
    [0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0]
]
labels2 = ['T', 'M', 'S', 'H', 'C']

print("Example 2:")
hamiltonian_cycle(graph2, labels2)
