import unittest, string, math, random

from solution import Graph, Vertex


class GraphTests(unittest.TestCase):

    def test_bfs(self):
        graph = Graph()

        # (1) test on empty graph
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (2) test on graph missing begin or dest
        graph.add_to_graph('a')
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))
        subject = graph.bfs('b', 'a')
        self.assertEqual(subject, ([], 0))

        # (3) test on graph with both vertices but no path
        graph.add_to_graph('b')
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (4) test on single edge
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, (['a', 'b'], 331))

        # (5) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        subject = graph.bfs('a', 'c')
        self.assertEqual(subject, (['a', 'b', 'c'], 431))

        # (6) test on edge triangle and ensure one-edge path is taken
        # (bfs guarantees fewest-edge path, not least-weighted path)
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        graph.add_to_graph('a', 'c', 999)
        subject = graph.bfs('a', 'c')
        self.assertEqual(subject, (['a', 'c'], 999))

        # (7) test on grid figure-8 and ensure fewest-edge path is taken
        graph = Graph(csvf='test_csvs/bfs/7.csv')

        subject = graph.bfs('bottomleft', 'topleft')
        self.assertEqual(subject, (['bottomleft', 'midleft', 'topleft'], 2))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('bottomright', 'topright')
        self.assertEqual(subject, (['bottomright', 'midright', 'topright'], 2))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('bottomleft', 'topright')
        self.assertIn(subject[0], [['bottomleft', 'midleft', 'topleft', 'topright'],
                                   ['bottomleft', 'midleft', 'midright', 'topright'],
                                   ['bottomleft', 'bottomright', 'midright', 'topright']])
        self.assertEqual(subject[1], 3)

        # (8) test on example graph from Onsay's slides, starting from vertex A
        # see bfs_graph.png
        graph = Graph(csvf='test_csvs/bfs/8.csv')

        subject = graph.bfs('a', 'd')
        self.assertEqual(subject, (['a', 'b', 'd'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'f')
        self.assertEqual(subject, (['a', 'c', 'f'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'h')
        self.assertEqual(subject, (['a', 'e', 'h'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'g')
        self.assertEqual(subject, (['a', 'e', 'g'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'i')
        self.assertIn(subject[0], [['a', 'e', 'h', 'i'], ['a', 'e', 'g', 'i']])
        self.assertEqual(subject[1], 6)

        # (9) test path which does not exist
        graph.unvisit_vertices()  # mark all unvisited
        graph.add_to_graph('z')
        subject = graph.bfs('a', 'z')
        self.assertEqual(subject, ([], 0))

    def test_a_star(self):

        # PART ONE -- SMALLER TEST CASES

        # === Edge Cases === #

        # (1) test on empty graph
        graph = Graph()
        subject = graph.a_star('a', 'b', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))

        # (2) start/end vertex does not exist
        graph = Graph()
        graph.add_to_graph('a')
        # (2.1) start vertex
        subject = graph.a_star('b', 'a', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))
        # (2.2) end vertex
        subject = graph.a_star('a', 'b', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))
        # (2.3) Neither vertex exists (Also tested in 3)
        subject = graph.a_star('b', 'c', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))

        # (3) test for path which does not exist
        graph = Graph()
        graph.add_to_graph('a', 'b')
        subject = graph.a_star('b', 'a', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))

        # === (A) Grid graph tests ===#
        graph = Graph()

        # (1) test on nxn grid from corner to corner: should shoot diagonal
        # (shortest path is unique, so each heuristic will return the same path)
        grid_size = 5
        for x in range(grid_size):
            for y in range(grid_size):
                idx = f"{x},{y}"
                graph.vertices[idx] = Vertex(idx, x, y)
                graph.size += 1

        for x in range(grid_size):
            for y in range(grid_size):
                if x < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                    graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                if y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                    graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                if x < grid_size - 1 and y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            subject = graph.a_star('0,0', '4,4', metric)
            self.assertEqual(subject[0], ['0,0', '1,1', '2,2', '3,3', '4,4'])
            self.assertAlmostEqual(subject[1], (grid_size - 1) * math.sqrt(2))
            graph.unvisit_vertices()

        # (2) test on nxn grid with penalty for shooting diagonal
        # (shortest path is not unique, so each heuristic will return a different path)
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        subject = graph.a_star('0,0', '4,4', Vertex.euclidean_distance)
        self.assertEqual(subject, (['0,0', '1,0', '1,1', '2,1', '2,2', '3,2', '3,3', '4,3', '4,4'], 8))
        graph.unvisit_vertices()
        subject = graph.a_star('0,0', '4,4', Vertex.taxicab_distance)
        self.assertEqual(subject, (['0,0', '1,0', '2,0', '3,0', '4,0', '4,1', '4,2', '4,3', '4,4'], 8))
        graph.unvisit_vertices()

        # === (B) Tollway graph tests ===#
        graph = Graph(csvf='test_csvs/astar/tollway_comprehensive_2.csv')
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        # UMCOMMENT TO SEE PLOT
        # graph.plot_show = True
        # graph.plot()

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            # (3) test Franklin Grove to Northbrook shortest path in both directions
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Franklin Grove', 'Northbrook', metric)
            solution = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 22)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Northbrook', 'Franklin Grove', metric)
            solution = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 22)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            # (4) test Franklin Grove to Joliet shortest path - bypass expensive tollway path
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Franklin Grove', 'Joliet', metric)
            solution = (['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Joliet', 'Franklin Grove', metric)
            solution = (['Joliet', 'E', 'D', 'H', 'G', 'B', 'A', 'Franklin Grove'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            # (5) test Joliet to Chicago shortest path - bypass expensive tollway path
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Joliet', 'Chicago', metric)
            solution = (['Joliet', 'E', 'D', 'H', 'G', 'J', 'K', 'L', 'Chicago'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Chicago', 'Joliet', metric)
            solution = (['Chicago', 'L', 'K', 'J', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            # (6) test Northbrook to Belvidere - despite equal path lengths, A* heuristic will always prefer search to the left
            # (both heuristics will prefer the same path)
            subject = graph.a_star('Northbrook', 'Belvidere', metric)
            solution = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 8)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Belvidere', 'Northbrook', metric)
            solution = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 8)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

        # PART 2 -- BIGGER TEST CASES

        # === (C) Random graph tests ===#
        # (1) initialize vertices of Euclidean and Taxicab weighted random graphs
        random.seed(331)
        probability = 0.5  # probability that two vertices are connected
        e_graph, t_graph = Graph(), Graph()
        vertices = []
        for s in string.ascii_lowercase:
            x, y = random.randint(0, 100), random.randint(0, 100)
            vertex = Vertex(s, x, y)
            vertices.append(vertex)
            e_graph.vertices[s], t_graph.vertices[s] = vertex, vertex
            e_graph.size += 1
            t_graph.size += 1

        # (2) construct adjacency matrix with edges weighted by appropriate distance metric
        e_matrix = [[None] + [s for s in string.ascii_lowercase]]
        t_matrix = [[None] + [s for s in string.ascii_lowercase]]
        for i in range(1, len(e_matrix[0])):
            e_row = [e_matrix[0][i]]
            t_row = [t_matrix[0][i]]
            for j in range(1, len(e_matrix[0])):
                connect = (random.random() < probability)  # connect if random draw in (0,1) < probability
                e_weighted_dist, t_weighted_dist = None, None
                if i != j and connect:
                    e_dist = vertices[i - 1].euclidean_distance(vertices[j - 1])
                    t_dist = vertices[i - 1].taxicab_distance(vertices[j - 1])
                    weight = (random.randint(1, 10))  # choose a random weight between 1 and 9
                    e_weighted_dist = e_dist * weight  # create realistic weighted dist
                    t_weighted_dist = t_dist * weight  # create realistic weighted dist
                e_row.append(e_weighted_dist)
                t_row.append(t_weighted_dist)
            e_matrix.append(e_row)
            t_matrix.append(t_row)
        e_graph.matrix2graph(e_matrix)
        t_graph.matrix2graph(t_matrix)

        # (3) define helper function to check validity of search result
        def is_valid_path(graph, search_result):
            path, dist = search_result
            length = 0
            for i in range(len(path) - 1):
                begin, end = path[i], path[i + 1]
                edge = graph.get_edge_by_ids(begin, end)
                if edge is None:
                    return False  # path contains some edge not in the graph
                length += edge[2]
            return length == dist  # path consists of valid edges: return whether length matches

        # (4) test all 26 x 26 pairwise A* traversals across random matrix and ensure they return valid paths w/o error
        for begin in vertices:
            for end in vertices:
                if begin != end:
                    subject = e_graph.a_star(begin.id, end.id, Vertex.euclidean_distance)
                    self.assertTrue(is_valid_path(e_graph, subject))
                    e_graph.unvisit_vertices()

                    subject = t_graph.a_star(begin.id, end.id, Vertex.taxicab_distance)
                    self.assertTrue(is_valid_path(t_graph, subject))
                    t_graph.unvisit_vertices()

    def test_application_basic(self):

        # (1) test empty graph
        graph = Graph()
        self.assertEqual((None, None), graph.tollways_algorithm('A', 'B', 5))

        # (2) test on graph missing begin or dest
        graph.add_to_graph('A')
        self.assertEqual((None, None), graph.tollways_algorithm('A', 'B', 5))
        self.assertEqual((None, None), graph.tollways_algorithm('B', 'A', 5))

        # (3) test one coupon
        graph = Graph()
        # (A, B, 2) -> City A to City B , costs 2
        graph.add_to_graph('A', 'B', 2)
        graph.add_to_graph('A', 'C', 6)
        graph.add_to_graph('B', 'D', 6)
        graph.add_to_graph('B', 'E', 8)
        graph.add_to_graph('C', 'E', 4)
        graph.add_to_graph('D', 'E', 1)

        self.assertEqual((1, 1), graph.tollways_algorithm('A', 'B', 1))
        self.assertEqual((3, 1), graph.tollways_algorithm('A', 'C', 1))
        self.assertEqual((5, 1), graph.tollways_algorithm('A', 'D', 1))
        self.assertEqual((6, 1), graph.tollways_algorithm('A', 'E', 1))
        # No path exist between E and B (cost is infinite)
        self.assertEqual((None, None), graph.tollways_algorithm('E', 'B', 1))

        # (4) test two coupons
        graph = Graph()
        graph.add_to_graph('A', 'B', 2)
        graph.add_to_graph('A', 'C', 8)
        graph.add_to_graph('A', 'D', 8)
        graph.add_to_graph('B', 'D', 6)
        graph.add_to_graph('B', 'C', 12)
        graph.add_to_graph('B', 'E', 5)
        graph.add_to_graph('C', 'E', 6)
        graph.add_to_graph('D', 'C', 2)

        self.assertEqual((1, 1), graph.tollways_algorithm('A', 'B', 2))
        self.assertEqual((4, 1), graph.tollways_algorithm('A', 'C', 2))
        self.assertEqual((4, 1), graph.tollways_algorithm('A', 'D', 2))
        self.assertEqual((3, 2), graph.tollways_algorithm('A', 'E', 2))

        # (5) test mix coupons
        graph = Graph()
        graph.add_to_graph('A', 'B', 3)
        graph.add_to_graph('A', 'E', 6)
        graph.add_to_graph('A', 'D', 4)
        graph.add_to_graph('A', 'F', 12)
        graph.add_to_graph('B', 'E', 4)
        graph.add_to_graph('B', 'C', 1)
        graph.add_to_graph('C', 'E', 3)
        graph.add_to_graph('D', 'F', 6)
        graph.add_to_graph('E', 'F', 3)
        
        self.assertEqual((6, 0), graph.tollways_algorithm('A', 'E', 0))
        self.assertEqual((3, 1), graph.tollways_algorithm('A', 'E', 1))
        self.assertEqual((3, 1), graph.tollways_algorithm('A', 'E', 2))
        self.assertEqual((2, 3), graph.tollways_algorithm('A', 'E', 3))
        self.assertEqual((9, 0), graph.tollways_algorithm('A', 'F', 0))
        self.assertEqual((6, 1), graph.tollways_algorithm('A', 'F', 1))
        self.assertEqual((4, 2), graph.tollways_algorithm('A', 'F', 2))
        self.assertEqual((3, 4), graph.tollways_algorithm('A', 'F', 4))
        self.assertEqual((None, None), graph.tollways_algorithm('E', 'B', 0))

        # (6) test no coupons, shortest path should be the same as A* algorithm
        graph = Graph()
        graph.add_to_graph('A', 'B', 3)
        graph.add_to_graph('A', 'E', 6)
        graph.add_to_graph('A', 'D', 4)
        graph.add_to_graph('A', 'F', 12)
        graph.add_to_graph('B', 'E', 4)
        graph.add_to_graph('B', 'C', 1)
        graph.add_to_graph('C', 'E', 3)
        graph.add_to_graph('D', 'F', 6)
        graph.add_to_graph('E', 'F', 3)
        self.assertEqual((3, 0), graph.tollways_algorithm('A', 'B', 0))
        self.assertEqual((4, 0), graph.tollways_algorithm('A', 'C', 0))
        self.assertEqual((4, 0), graph.tollways_algorithm('A', 'D', 0))
        self.assertEqual((6, 0), graph.tollways_algorithm('A', 'E', 0))
        self.assertEqual((9, 0), graph.tollways_algorithm('A', 'F', 0))
        self.assertEqual((None, None), graph.tollways_algorithm('E', 'B', 0))

        # Test with A* (zero metric -> normal dijkstra)
        path, dist = graph.a_star('A', 'F', metric=lambda u, v: 0)
        self.assertEqual((dist, 0), graph.tollways_algorithm('A', 'F', 0))
        
        path, dist = graph.a_star('A', 'E', metric=lambda u, v: 0)
        self.assertEqual((dist, 0), graph.tollways_algorithm('A', 'E', 0))

        path, dist = graph.a_star('B', 'F', metric=lambda u, v: 0)
        self.assertEqual((dist, 0), graph.tollways_algorithm('B', 'F', 0))

        path, dist = graph.a_star('B', 'E', metric=lambda u, v: 0)
        self.assertEqual((dist, 0), graph.tollways_algorithm('B', 'E', 0))

        # (7) Test if the street is a 2 way street and have a cycle
        graph = Graph()
        graph.add_to_graph('A', 'B', 6)
        graph.add_to_graph('B', 'C', 2)
        graph.add_to_graph('C', 'D', 6)
        graph.add_to_graph('D', 'A', 4)
        graph.add_to_graph('B', 'A', 4)
        graph.add_to_graph('A', 'D', 2)
        graph.add_to_graph('D', 'C', 8)
        graph.add_to_graph('C', 'B', 2)

        # Here is the graph representation. Each number from each side of the vertex represents the cost of the edge
        # from tail to head.
        ##############################
        #  A   (4) <----> (6)   B
        # (4)                  (2)
        #  ^                    ^
        #  |                    |
        #  v                    v
        # (2)                  (2)
        #  D   (6) <---> (8)   C
        self.assertEqual((6, 0), graph.tollways_algorithm('A', 'B', 0))
        self.assertEqual((6, 0), graph.tollways_algorithm('B', 'D', 0))
        self.assertEqual((4, 1), graph.tollways_algorithm('B', 'D', 1))
        self.assertEqual((1, 1), graph.tollways_algorithm('A', 'D', 1))  # Going from A to D is better

        graph = Graph()
        nodes = [chr(i) for i in range(65, 85)]

        for i in range(1, len(nodes)):
            graph.add_to_graph(nodes[i-1], nodes[i], 1)

        graph.add_to_graph(nodes[-1], "Z", 1)
        graph.add_to_graph(nodes[0], "Z", len(nodes)+1)

        self.assertEqual((20, 0), graph.tollways_algorithm('A', 'Z', 0))
        self.assertEqual((10, 1), graph.tollways_algorithm('A', 'Z', 1))
        self.assertEqual((10, 1), graph.tollways_algorithm('A', 'Z', 2))
        
    def test_application_comprehensive(self):
        # (8) Test a large graph
        graph = Graph(csvf='test_csvs/astar/tollway_comprehensive_1.csv')

        # Test all-way shortest path with various coupons and (start, end) nodes
        expected = [
            # Zero coupons
            [(2.0, 0), (4.0, 0), (6.0, 0), (8.0, 0), (10.0, 0), (12.0, 0), (12.0, 0), (8.0, 0), (6.0, 0), (4.0, 0),
             (258.0, 0), (130.0, 0), (66.0, 0), (34.0, 0), (18.0, 0), (10.0, 0), (6.0, 0), (4.0, 0), (2.0, 0), (2.0, 0),
             (4.0, 0), (6.0, 0), (8.0, 0), (10.0, 0), (8.0, 0), (6.0, 0), (4.0, 0), (66.0, 0), (34.0, 0), (18.0, 0),
             (10.0, 0), (6.0, 0), (4.0, 0), (2.0, 0), (2.0, 0), (4.0, 0), (6.0, 0), (8.0, 0), (6.0, 0), (4.0, 0),
             (18.0, 0), (10.0, 0), (6.0, 0), (4.0, 0), (2.0, 0), (2.0, 0), (4.0, 0), (6.0, 0), (4.0, 0), (6.0, 0),
             (4.0, 0), (2.0, 0), (2.0, 0), (4.0, 0), (2.0, 0)],
            # One coupon
            [(1.0, 1), (2.0, 1), (4.0, 1), (6.0, 1), (8.0, 1), (10.0, 1), (8.0, 1), (6.0, 1), (4.0, 1), (3.0, 1),
             (130.0, 1), (66.0, 1), (34.0, 1), (18.0, 1), (10.0, 1), (6.0, 1), (4.0, 1), (2.0, 1), (1.0, 1), (1.0, 1),
             (2.0, 1), (4.0, 1), (6.0, 1), (8.0, 1), (6.0, 1), (4.0, 1), (3.0, 1), (34.0, 1), (18.0, 1), (10.0, 1),
             (6.0, 1), (4.0, 1), (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (4.0, 1), (6.0, 1), (4.0, 1), (3.0, 1),
             (10.0, 1), (6.0, 1), (4.0, 1), (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (4.0, 1), (3.0, 1), (4.0, 1),
             (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (1.0, 1)],
            # Two coupons
            [(1.0, 1), (2.0, 1), (3.0, 2), (4.0, 2), (6.0, 2), (8.0, 2), (7.0, 2), (5.0, 2), (3.0, 2), (2.0, 2),
             (129.0, 2), (65.0, 2), (33.0, 2), (17.0, 2), (9.0, 2), (5.0, 2), (3.0, 2), (2.0, 1), (1.0, 1), (1.0, 1),
             (2.0, 1), (3.0, 2), (4.0, 2), (6.0, 2), (5.0, 2), (3.0, 2), (2.0, 2), (33.0, 2), (17.0, 2), (9.0, 2),
             (5.0, 2), (3.0, 2), (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (3.0, 2), (4.0, 2), (3.0, 2), (2.0, 2),
             (9.0, 2), (5.0, 2), (3.0, 2), (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (3.0, 2), (2.0, 2), (3.0, 2),
             (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (1.0, 1)],
            # Three coupons
            [(1.0, 1), (2.0, 1), (3.0, 2), (4.0, 2), (5.0, 3), (6.0, 3), (6.0, 3), (4.0, 3), (3.0, 2), (2.0, 2),
             (129.0, 2), (65.0, 2), (33.0, 2), (17.0, 2), (9.0, 2), (5.0, 2), (3.0, 2), (2.0, 1), (1.0, 1), (1.0, 1),
             (2.0, 1), (3.0, 2), (4.0, 2), (5.0, 3), (4.0, 3), (3.0, 2), (2.0, 2), (33.0, 2), (17.0, 2), (9.0, 2),
             (5.0, 2), (3.0, 2), (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (3.0, 2), (4.0, 2), (3.0, 2), (2.0, 2),
             (9.0, 2), (5.0, 2), (3.0, 2), (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (3.0, 2), (2.0, 2), (3.0, 2),
             (2.0, 1), (1.0, 1), (1.0, 1), (2.0, 1), (1.0, 1)]
        ]

        for coupons in range(4):
            nodes = list("ABCDEFGHIJK")
            expected_with_i_coupons = iter(expected[coupons])
            for i in range(len(nodes)):
                start = nodes[i]
                for j in range(i+1, len(nodes)):
                    end = nodes[j]
                    self.assertEqual(next(expected_with_i_coupons), graph.tollways_algorithm(start, end, coupons))

        # (9) Test another large graph
        random.seed(331)
        graph = Graph(csvf='test_csvs/astar/tollway_comprehensive_2.csv')

        # Simple test case
        roads = ['Franklin Grove', 'Willow Creek', 'Burr Ridge', 'Joliet', 'Belvidere', 'Northbrook', 'Chicago']
        self.assertEqual((12, 5), graph.tollways_algorithm('Franklin Grove', 'Chicago', 5))
        self.assertEqual((12, 5), graph.tollways_algorithm('Willow Creek', 'Chicago', 6))
        self.assertEqual((16, 6), graph.tollways_algorithm('Joliet', 'Chicago', 6))

        # Test all way shortest path with some coupons
        expected = [(8.0, 2), (8.0, 2), (8.0, 2), (8.0, 2), (8.0, 2), (16.0, 5), (16.0, 5), (16.0, 5),
                    (16.0, 5), (16.0, 5), (16.0, 5), (16.0, 5), (16.0, 5), (16.0, 5), (16.0, 5), (18.0, 1),
                    (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4),
                    (10.0, 4), (14.0, 4), (12.0, 5), (12.0, 5), (12.0, 5), (12.0, 5), (8.0, 2), (8.0, 2),
                    (8.0, 2), (8.0, 2), (8.0, 2), (10.0, 2), (10.0, 2), (10.0, 2), (14.0, 1), (21.0, 0),
                    (10.0, 2), (10.0, 2), (14.0, 1), (10.0, 2), (10.0, 2), (10.0, 4), (10.0, 4), (10.0, 4),
                    (10.0, 4), (10.0, 4), (12.0, 3), (10.0, 4), (10.0, 4), (18.0, 1), (10.0, 4), (22.0, 1),
                    (12.0, 5), (22.0, 1), (12.0, 5), (12.0, 5), (16.0, 5), (16.0, 5), (16.0, 5), (21.0, 3),
                    (16.0, 5), (10.0, 2), (10.0, 2), (14.0, 1), (10.0, 2), (10.0, 2), (0.0, 0), (0.0, 0),
                    (0.0, 0), (0.0, 0), (0.0, 0), (31.0, 0), (14.0, 5), (14.0, 5), (14.0, 5), (14.0, 5),
                    (16.0, 4), (14.0, 5), (14.0, 5), (24.0, 1), (24.0, 1), (16.0, 6), (16.0, 6), (19.0, 4), (16.0, 6),
                    (35.0, 0), (16.0, 5), (16.0, 5), (16.0, 5), (16.0, 5), (28.0, 1), (10.0, 2), (10.0, 2), (10.0, 2),
                    (10.0, 2), (10.0, 2), (0.0, 0), (0.0, 0), (0.0, 0), (0.0, 0), (0.0, 0), (14.0, 5), (14.0, 5),
                    (14.0, 5), (14.0, 5), (24.0, 1), (14.0, 5), (14.0, 5), (14.0, 5), (14.0, 5), (14.0, 5), (16.0, 6),
                    (16.0, 6), (16.0, 6), (16.0, 6), (16.0, 6), (10.0, 4), (15.0, 2), (10.0, 4), (10.0, 4), (10.0, 4),
                    (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (14.0, 5), (14.0, 5), (16.0, 4), (14.0, 5),
                    (14.0, 5), (14.0, 5), (14.0, 5), (14.0, 5), (16.0, 4), (14.0, 5), (4.0, 2), (4.0, 2), (6.0, 1),
                    (4.0, 2), (4.0, 2), (2.0, 1), (2.0, 1), (2.0, 1), (2.0, 1), (4.0, 0), (10.0, 4), (10.0, 4),
                    (10.0, 4), (18.0, 1), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (10.0, 4), (14.0, 5),
                    (14.0, 5), (14.0, 5), (14.0, 5), (14.0, 5), (18.0, 3), (16.0, 4), (14.0, 5), (14.0, 5), (14.0, 5),
                    (4.0, 2), (4.0, 2), (4.0, 2), (4.0, 2), (4.0, 2), (2.0, 1), (2.0, 1), (2.0, 1), (2.0, 1), (4.0, 0),
                    (12.0, 5), (16.0, 3), (12.0, 5), (12.0, 5), (19.0, 2), (12.0, 5), (12.0, 5), (12.0, 5), (12.0, 5),
                    (12.0, 5), (16.0, 6), (16.0, 6), (16.0, 6), (16.0, 6), (16.0, 6), (16.0, 6), (16.0, 6), (16.0, 6),
                    (16.0, 6), (28.0, 1), (2.0, 1), (2.0, 1), (2.0, 1), (2.0, 1), (2.0, 1), (2.0, 1), (2.0, 1),
                    (2.0, 1), (2.0, 1), (2.0, 1)]
        expected_result = iter(expected)
        for st in roads:
            for ed in roads:
                if st == ed:
                    continue
                for _ in range(5):
                    coupons = random.randint(0, 20)
                    self.assertEqual(next(expected_result), graph.tollways_algorithm(st, ed, coupons),
                                     msg=f"Error: Route from {st} to {ed} with {coupons} coupon(s)")


if __name__ == '__main__':
    unittest.main()
