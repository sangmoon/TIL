class BFS:

    def __init__(self):
        pass

    @staticmethod
    def list_to_graph(lst, rows, coloums):
        graph = {}
        for j in range(coloums):
            for i in range(rows):
                graph[(i, j)] = []
                if 0 <= i - 1 < rows and 0 <= j < coloums and lst[i-1][j] == 1:
                    graph[(i, j)].append((i-1, j))
                
                if 0 <= i + 1 < rows and 0 <= j < coloums and lst[i+1][j] == 1:
                    graph[(i, j)].append((i+1, j))

                if 0 <= i < rows and 0 <= j - 1 < coloums and lst[i][j-1] == 1:
                    graph[(i, j)].append((i, j-1))

                if 0 <= i < rows and 0 <= j + 1 < coloums and lst[i][j+1] == 1:
                    graph[(i, j)].append((i, j+1))             
                
        return graph

    def test_path(self, graph, start, end):
        explored = []
        queue = [[start]]

        if start is end:
            print("start is end! easy")

        while(queue):
            path = queue.pop(0)
            node = path[-1]
            if node not in explored:
                neighbours = graph[node]
                # go through all neighbour nodes, construct a new path and
                # push it into the queue
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    # return path if neighbour is goal
                    if neighbour == end:
                        return new_path
                # mark node as explored
                explored.append(node)

        # in case there's no path between the 2 nodes
        return "So sorry, but a connecting path doesn't exist :("


if __name__ == "__main__":
    MAP = [[1, 1, 1, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0, 1], [0, 1, 1, 0, 1], [0, 1, 1, 1, 1], ]

    bfs = BFS()
    print(bfs.test_path(BFS.list_to_graph(MAP, 5, 5), (0, 0), (4, 4)))
