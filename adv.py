from room import Room
from player import Player
from world import World
from util import Queue

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
traversal_graph = {}
traversal_grid = []
rooms_set = set([v.id for k, v in world.rooms.items()])
visited_rooms = set()

for _ in range(len(world.room_grid)):
    traversal_grid.append([0] * len(world.room_grid))


current_room = player.current_room

q = Queue()
q.enqueue(current_room.get_exits())
path = []
random_move = ""
room_id = -1
finished = False

while q.size() > 0 and not finished:
    visited_rooms.add(player.current_room.id)
    if not len(rooms_set.difference(visited_rooms)):
        break
    moves = q.dequeue()

    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = {}
        for move in moves:
            traversal_graph[player.current_room.id][move] = '?'

    if random_move == 'w':
        traversal_graph[player.current_room.id]['e'] = room_id
    elif random_move == 'e':
        traversal_graph[player.current_room.id]['w'] = room_id
    elif random_move == 's':
        traversal_graph[player.current_room.id]['n'] = room_id
    elif random_move == 'n':
        traversal_graph[player.current_room.id]['s'] = room_id
    
    room_id = player.current_room.id
    moves = [move for move in moves if traversal_graph[room_id][move] == '?']

    if len(moves):
        random_move = random.choice(moves)
        if traversal_graph[room_id][random_move] == '?':
            player.travel(random_move)
            visited_rooms.add(player.current_room.id)
            x, y = player.current_room.get_coords()
            traversal_grid[x][y] += 1
            path.append(random_move)
            traversal_path.append(random_move)
            traversal_graph[room_id][random_move] = player.current_room.id
            
            q.enqueue(player.current_room.get_exits())
    else:
        if len(path):
            random_move = ""
            while not len([value for key, value in traversal_graph[player.current_room.id].items() if value == "?"]) and len(path):
                move = path.pop()
                if move == 'w':
                    move = 'e'
                elif move == 'e':
                    move = 'w'
                elif move == 's':
                    move = 'n'
                elif move == 'n':
                    move = 's'
                player.travel(move)
                visited_rooms.add(player.current_room.id)
                x, y = player.current_room.get_coords()
                traversal_grid[x][y] += 1
                traversal_path.append(move)
            q.enqueue(player.current_room.get_exits())



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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
