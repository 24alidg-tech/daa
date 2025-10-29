# Graph Coloring using Backtracking

def is_safe(v, graph, color, c):
    """Check if color c can be assigned to vertex v"""
    for i in range(len(graph)):
        if graph[v][i] == 1 and color[i] == c:
            return False
    return True


def graph_coloring_util(graph, m, color, v):
    """Recursive utility to solve coloring problem"""
    if v == len(graph):
        return True

    for c in range(1, m + 1):
        if is_safe(v, graph, color, c):
            color[v] = c
            if graph_coloring_util(graph, m, color, v + 1):
                return True
            color[v] = 0  # Backtrack
    return False


def graph_coloring(graph, m):
    """Main function to solve the problem"""
    color = [0] * len(graph)
    if not graph_coloring_util(graph, m, color, 0):
        print("No solution exists")
        return
    print("Solution exists: Following are the assigned colors")
    print(color)


# Example adjacency matrix for Graph 1
graph1 = [
    [0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 0, 1, 1, 0]
]

m = 3  # Number of available colors (frequencies)
graph_coloring(graph1, m)

graph2 = [
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0]
]

graph_coloring(graph2, 5)
