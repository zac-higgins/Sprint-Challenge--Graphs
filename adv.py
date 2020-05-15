from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# ---------- Traversal Algorithm ---------#
def dft(current_room):
    opposites = {
        'n': 's',
        'e': 'w',
        's': 'n',
        'w': 'e'
    }
    path = []
    visited = set()
    def search(current_room, previous_room, last_direction_traveled=None):
        if len(visited) < len(room_graph):
            exits = current_room.get_exits()
            visited.add(current_room)
            # randomized_indexes = random.sample(range(0, len(exits)), len(exits))
            for direction in exits:
                # direction = exits[index]
                next_room = current_room.get_room_in_direction(direction)
                if next_room not in visited and len(exits) > 2:
                    path.append(direction)
                    search(next_room, current_room, direction)
                elif next_room not in visited and len(exits) <= 2:
                    path.append(direction)
                    search(next_room, None, direction)
                if next_room in visited and next_room == previous_room:
                    path.append(direction)
                    search(next_room, None)
            if last_direction_traveled is not None:
                path.append(opposites[last_direction_traveled])
    search(current_room, None)
    return path

# ---------- Map Traversal ---------#
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = dft(player.current_room)
print(f"Traversal Path: {traversal_path}")

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
