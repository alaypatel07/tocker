INFINITE = 9999


class Node:
    def __init__(self, name, adjacency_list):
        self.name = int(name)
        self.adjacency_list = adjacency_list
        self.distance_from_source = INFINITE
        self.parents = []
        self.hops = 0

    def adjacent(self, adj):
        self.adjacency_list.append(adj)

    def set_cost(self, c):
        self.distance_from_source = c

    def __repr__(self):
        return str(self.name) + " with neighbours --- " + " ".join(
            [str(i) for i in self.adjacency_list]) + " cost " + str(self.distance_from_source) + " hops " + str(
            self.hops) + " parent " + str([str(i) for i in self.parents])

    def add_parent(self, parent):
        self.parents.append(parent)


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n'.join([str(i) for i in self.queue])

    def insert(self, node):
        self.queue.append(node)

    def extract_min(self):
        minimum = INFINITE + 1
        minimum_element = None
        for element in self.queue:
            if element.distance_from_source <= minimum:
                minimum = element.distance_from_source
                minimum_element = element
        self.queue.remove(minimum_element)
        return minimum_element

    def decrease_key(self, node, c, parent):
        for element in self.queue:
            if element.name == node.name:
                node.distance_from_source = c
                node.hops += 1
                node.parents = [parent]

    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False


def build_priority_queue(nodes):
    pq = PriorityQueue()
    for node in nodes:
        pq.insert(node)
    return pq


def run_dijkstra(pq, w, nodes):
    discovered = []
    while not pq.empty():
        u = pq.extract_min()
        c = u.distance_from_source
        discovered.append(u)
        for v in u.adjacency_list:
            if nodes[v].distance_from_source > c + w[u.name][v]:
                pq.decrease_key(nodes[v], c + w[u.name][v], u.name)
            elif nodes[v].distance_from_source == c + w[u.name][v]:
                nodes[v].add_parent(u.name)
    return discovered


# def print_parents(nodes, source, destination):
#     if source == destination:
#         return str(source)
#     paths = []
#     for parent in nodes[destination].parents:
#         path = print_parents(nodes, source, parent)
#         path = [p + " " + str(destination) for p in path]
#         for p in path:
#             paths.append(p)
#     return paths

def print_parents(nodes, source, destination):
    if source == destination:
        return [[source]]
    paths = []
    for parent in nodes[destination].parents:
        path = print_parents(nodes, source, parent)
        for p in path:
            p.append(destination)
            paths.append(p)
    return paths


if __name__ == '__main__':
    v, e = raw_input().split(" ")
    v = int(v)
    e = int(e)
    if (not 1 <= v <= 50) or (not 1 <= e <= 100):
        exit(2)
    nodes = [Node(i, []) for i in range(v)]
    w = [[0 for _ in range(v)] for _ in range(v)]
    adjacency_list = [list() for _ in range(v)]
    for i in range(e):
        source, destination, cost_1 = raw_input().split(" ")
        source = int(source)
        destination = int(destination)
        cost_1 = int(cost_1)
        # if (cost < 0) or (not 1 <= source <= 50) or (not 1 <= destination <= 50):
        #     exit(2)
        w[source][destination] = cost_1
        w[destination][source] = cost_1
        nodes[source].adjacent(destination)
        nodes[destination].adjacent(source)
        adjacency_list[destination].append(source)
        adjacency_list[source].append(destination)

    source, destination = raw_input().split(" ")
    source = int(source)
    nodes[source].set_cost(0)
    pq = build_priority_queue(nodes)
    destination = int(destination)
    discovered_nodes = run_dijkstra(pq, w, nodes)
    # pprint(nodes)
    print nodes[destination].distance_from_source
    paths = print_parents(nodes, source, destination)
    path = min(paths, key=len)
    minimum_length_path = len(path)
    shortest_paths = []
    for path in paths:
        if len(path) == minimum_length_path:
            shortest_paths.append(path)
    print " ".join([str(p) for p in min(shortest_paths)])
