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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
Goal_traversal_path = ['n', 'n', 's', 's', 'e', 'e', 'w', 'w', 's', 's', 'n', 'n', 'w', 'w']

# ---------- Graph Setup ---------#
from util import Queue, Stack

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
        self.opposites = {
            'n': 's',
            'e': 'w',
            's': 'n',
            'w': 'e'
        }

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
    def dft(self, current_room):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        '''
        variables: previous, current, direction
        '''
        possibility_path = []
        def search(current_room, visited=None, last_direction_traveled=None):
            nonlocal possibility_path
            exits = current_room.get_exits()
            if visited is None:
                visited = set()
            visited.add(current_room)
            for direction in exits:
                next_room = current_room.get_room_in_direction(direction)
                if next_room not in visited:
                    possibility_path.append(direction)
                    search(next_room, visited, direction)
                    # traversal_path.append(possibility_path)
                    # for item in possibility_path:
                    #     traversal_path.append(item)
            if last_direction_traveled is not None:
                possibility_path.append(self.opposites[last_direction_traveled])
        # -----Currently doesn't account for forks of forks ------ #
                    # return_trip = reversed(possibility_path)
                    # for item in return_trip:
                    #     traversal_path.append(self.opposites[item])

            # possibility_path = []
                    # return_trip = []

        search(current_room)
        return possibility_path



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
traversal_path = graph.dft(player.current_room)
# print(f"Traversal Path: {traversal_path}")
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
