from room import Room
from player import Player
from world import World
# from search import Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# ---------- Graph Setup ---------#
from util import Queue, Stack

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set() # set of edges
        # print("vertex added!")

    def add_edge(self, room_id, directions):
        """
        Add a directed edge to the graph.
        """
        if room_id in self.vertices:
            self.vertices[room_id] = directions
        else:
            raise IndexError("Vertex does not exist in graph")

    def get_neighbors(self, room_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        current_room = world.rooms[room_id]
        exits = current_room.get_exits()
        neighbors = []
        for direction in exits:
            neighbor = current_room.get_room_in_direction(direction)
            neighbors.append(neighbor.id)
        return neighbors
    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        stack = Stack()
        stack.push(starting_vertex)
        visited = set()
        while stack.size() > 0:
            current_vertex = stack.pop()
            # print(current_vertex)
            if current_vertex not in visited:
                visited.add(current_vertex)
                # print(current_vertex)
                for next_vertex in self.get_neighbors(current_vertex):
                    stack.push(next_vertex)
        return visited
        # for vertex in visited:
        #     print(vertex)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        stack = Stack()
        stack.push(starting_vertex)
        visited = set()
        path = []
        while stack.size() > 0:
            current_vertex = stack.pop()
            if current_vertex == destination_vertex:
                path.append(current_vertex)
                return path
            if current_vertex not in visited:
                visited.add(current_vertex)
                path.append(current_vertex)
                for next_vertex in self.get_neighbors(current_vertex):
                    stack.push(next_vertex)

# ---------- Graph Setup ---------#

# ---------- Map Traversal ---------#
graph = Graph()
# print("rooms: ")
for room in world.rooms:
    graph.add_vertex(world.rooms[room].id)
    graph.add_edge(world.rooms[room].id, {'n': '?', 's': '?', 'w': '?', 'e': '?'})
    # print(f"{world.rooms[room].name} : {graph.vertices[world.rooms[room].id]}")
# print(world.rooms[0].get_exits())
# print(graph.get_neighbors(player.current_room.id))
print(graph.dft(player.current_room.id))
# ---------- Map Traversal ---------#


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
