# CS656 Final Research Project

# Written by Beck Gozdenovich


import heapq

def dspa(graph, source_node, dest_node):
    distances = {node: float('infinity') for node in graph}
    distances[source_node] = 0
    
    priority = [(0, source_node)]
    predecessors = {node: None for node in graph}

    while priority:
        current_distance, current_node = heapq.heappop(priority)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority, (distance, neighbor))

    shortest_path = []
    current_node = dest_node
    while current_node is not None:
        shortest_path.insert(0, current_node)
        current_node = predecessors[current_node]
    
    return shortest_path, distances[dest_node]


def kopa(graph, source_node, dest_node):
    length = 0
    source_cluster = {}
    dest_cluster = {}
    ch_cluster = graph[len(graph)-1]
    for c in range(len(graph)-1):
        if source_node in graph[c].keys():
            source_cluster = graph[c]

        if dest_node in graph[c].keys():
            dest_cluster = graph[c]

    if source_cluster == dest_cluster:
        path, length = dspa(source_cluster, source_node, dest_node)
        return path, length
    
    source_ch = ''
    dest_ch = ''
    for x in source_cluster.keys():
        for y in ch_cluster.keys():
            if x == y:
                source_ch = y
    for x in dest_cluster.keys():
        for y in ch_cluster.keys():
            if x == y:
                dest_ch = y

    sc_path, sc_dist = dspa(source_cluster, source_node, source_ch)
    dc_path, dc_dist = dspa(dest_cluster, dest_ch, dest_node)
    ch_path, ch_dist = dspa(ch_cluster, source_ch, dest_ch)

    sc_path.pop()
    ch_path.pop()

    length = sc_dist + ch_dist + dc_dist
    path = sc_path + ch_path + dc_path
    return path, length

cluster_b = {
    'A': {'B': 2, 'C': 3, 'E': 4},
    'B': {'A': 2, 'E': 3},
    'C': {'A': 3, 'E': 1, 'D': 5},
    'D': {'C': 5},
    'E': {'A': 4, 'B': 3, 'C': 1}
}

cluster_f = {
    'F': {'G': 3, 'I': 4},
    'G': {'F': 3, 'H': 1, 'I': 2},
    'H': {'G': 1, 'I': 5},
    'I': {'H': 5, 'G': 2}
}

cluster_j = {
    'J': {'L': 1, 'K': 4},
    'K': {'J': 4, 'N': 1, 'M': 6},
    'L': {'J': 1, 'M': 3},
    'M': {'L': 3, 'N': 4, 'K': 6},
    'N': {'M': 4, 'K': 1}
}

clusterheads = {
    'B': {'J': 1, 'F': 5},
    'F': {'B': 5, 'J': 3},
    'J': {'B': 1, 'F': 3}
}

topology = [cluster_b, cluster_f, cluster_j, clusterheads]
start_node = 'A'
end_node = 'D'
path, distance = kopa(topology, start_node, end_node)
print(f'The optimal communication distance between {start_node} and {end_node} is {distance} over the path: {path}')
