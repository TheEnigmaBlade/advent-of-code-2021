import sys
from collections import deque
from itertools import product
from pprint import pprint

import colorama
from colorama import Fore, Back, Style
colorama.init()

def load_map(name: str) -> list[list[int]]:
	with open(f"{name}.txt") as f:
		return [list(map(int, line.strip())) for line in f.readlines()]

map_weights = load_map("input")
map_width = len(map_weights[0])
map_height = len(map_weights)

def print_map(route: list[tuple[int, int]]):
	for y, row in enumerate(map_weights):
		for x, val in enumerate(row):
			if (x, y) in route:
				print(f"{Fore.BLUE}{val}{Style.RESET_ALL}", end="")
			else:
				print(f"{val}", end="")
		print()

Point = tuple[int, int]

def get_neighbors(p: Point) -> list[tuple[int, int]]:
	# noinspection PyTypeChecker
	return list(filter(None, [
		(p[0], p[1] + 1) if p[1] < map_height-1 else None,
		(p[0], p[1] - 1) if p[1] > 0 else None,
		(p[0] - 1, p[1]) if p[0] > 0 else None,
		(p[0] + 1, p[1]) if p[0] < map_width - 1 else None,
	]))

# Create vertex set
nodes: list[Point] = list(product(range(map_width), range(map_height)))
dist: dict[Point, int] = {n: sys.maxsize for n in nodes}
dist[(0, 0)] = 0
prev: dict[Point, Point] = {(0, 0): None}

def get_next_min():
	min_node = nodes[0]
	min_dist = dist[min_node]
	for n in nodes:
		if (d := dist[n]) < min_dist:
			min_node = n
			min_dist = d
	return min_node
		
# Create dist graph
while len(nodes) > 0:
	current_node = get_next_min()
	nodes.remove(current_node)
	current_dist = dist[current_node]
	
	for nb_node in get_neighbors(current_node):
		if nb_node in nodes:
			nb_dist = current_dist + map_weights[nb_node[1]][nb_node[0]]
			if nb_dist < dist[nb_node]:
				dist[nb_node] = nb_dist
				prev[nb_node] = current_node

# Find path
path = deque()
node = (map_width-1, map_height-1)
total_risk = dist[node]
while node is not None and node in prev:
	path.appendleft(node)
	node = prev[node]

print(f"Path: {path}")
print(f"Risk: {total_risk}")
print_map(list(path))
