from collections import deque


class Graph:
    vertices = {}

    def __init__(self, vertices=dict):
        if not bool(self.vertices):
            self.vertices = vertices

    def add_vertex(self, vertex_name):
        if vertex_name not in self.vertices:
            self.vertices[vertex_name] = []

    def add_edge(self, v1_from, v2_to):
        # if v1_from in self.vertices and v2_to in self.vertices:
        self.vertices[v1_from].append(v2_to)

    def file_to_graph(self):
        file = open("input.txt", "r")
        line = file.readline().replace(" ", "").strip()
        workers_number = int(line.__len__() ** 0.5)
        for j in range(0, workers_number):
            self.add_vertex(j)
        for i in range(0, line.__len__()):
            if line[i] == "Y":
                boss_number = i // workers_number
                worker_number = i % workers_number
                self.add_edge(boss_number, worker_number)

    def tree_to_file(self, tree):
        file = open("govern.out", "w")
        for v in tree:
            file.write(v + "\n")

    def graph_check(self):
        print("Checking")
        keys = set()
        values = set()
        for v in self.vertices:
            keys.add(v)
            for sub_v in self.vertices[v]:
                values.add(sub_v)
        if list(values - keys):
            print("Fixing...")
            for v in list(values - keys):
                self.add_vertex(v)
        print("Finish checking")

    def check_for_cyclic(self):
        path = set()

        def visit(vertex):
            path.add(vertex)
            for neighbour in self.vertices.get(vertex, ()):
                if neighbour in path or visit(neighbour):
                    return True
            path.remove(vertex)
            return False

        return any(visit(v) for v in self.vertices)

    def dfs_sort(self, start_vartice):
        visited = set()
        path = []
        order = []
        to_process = [start_vartice]
        while to_process:
            v = to_process.pop()
            if v not in visited:
                visited.add(v)
                to_process.extend(self.vertices[v])
                while path and v not in self.vertices[path[-1]]:
                    order.append(path.pop())
                path.append(v)
        return path + order[::-1]

    def calculate_salary(self):
        salaries = {}
        salaries_sum = 0
        for vertex in self.vertices:
            path = self.dfs_sort(vertex)
            if path.__len__() == 1:
                salary = 1
            else:
                salary = path.__len__() - 1
            salaries_sum += salary
            salaries[vertex] = salary
        salaries["sum"] = salaries_sum
        return salaries


g = {}
graph = Graph(g)
graph.file_to_graph()
print(graph.calculate_salary())
