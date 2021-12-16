import sys
from collections import deque
from itertools import product
from typing import NamedTuple, Optional
from pprint import pprint

import colorama
from colorama import Fore, Back, Style
colorama.init()

def load_map(name: str, multi: int) -> list[list[int]]:
	with open(f"{name}.txt") as f:
		big_map = [list(map(int, line.strip())) for line in f.readlines()]
		for line in big_map:
			extend_by = list(line)
			for _ in range(multi-1):
				extend_by = [1 if x + 1 > 9 else x + 1 for x in extend_by]
				line.extend(extend_by)
		extend_by = [row[:] for row in big_map]
		for _ in range(multi-1):
			for i in range(len(extend_by)):
				extend_by[i] = [1 if x + 1 > 9 else x + 1 for x in extend_by[i]]
			big_map.extend(extend_by)
		return big_map

map_weights = load_map("input", 5)
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
NodeInfo = NamedTuple("NodeInfo", dist=int, prev=Optional[Point], visited=bool)

def get_neighbors(p: Point) -> list[tuple[int, int]]:
	# noinspection PyTypeChecker
	return list(filter(None, [
		(p[0], p[1] + 1) if p[1] < map_height-1 else None,
		(p[0], p[1] - 1) if p[1] > 0 else None,
		(p[0] - 1, p[1]) if p[0] > 0 else None,
		(p[0] + 1, p[1]) if p[0] < map_width - 1 else None,
	]))

# Create node sets
nodes: list[Point] = list(product(range(map_width), range(map_height)))
node_info: dict[Point, NodeInfo] = {n: NodeInfo(sys.maxsize, None, False) for n in nodes}
node_info[(0, 0)] = NodeInfo(0, None, False)

def get_next_min() -> tuple[Point, NodeInfo]:
	min_node = nodes[0]
	min_info = node_info[min_node]
	for n in nodes:
		if (d := node_info[n]).dist < min_info.dist:
			min_node = n
			min_info = d
	return min_node, min_info

def solve_graph(start: Point) -> deque[Point]:
	progress_max = len(nodes)
	print(f"Searching {progress_max} nodes")
	progress = 0
	current_pct = 0
	
	# Create dist graph
	print("Solving graph")
	print("0%", end="")
	while len(nodes) > 0:
		current_node, current_info = get_next_min()
		nodes.remove(current_node)
		
		for nb_node in get_neighbors(current_node):
			if not (nb_info := node_info[nb_node]).visited:
				nb_dist = current_info.dist + map_weights[nb_node[1]][nb_node[0]]
				if nb_dist < nb_info.dist:
					node_info[nb_node] = NodeInfo(nb_dist, current_node, True)
		
		progress += 1
		new_pct = int(progress/progress_max*100)
		if new_pct > current_pct:
			current_pct = new_pct
			print(f"\r{current_pct}%", end="")
	
	# Find path
	print("Finding path")
	path = deque()
	node = (map_width-1, map_height-1)
	total_risk = node_info[node].dist
	while (info := node_info[node]).visited:
		path.appendleft(node)
		node = info.prev
	path.appendleft(start)
	
	print(f"Path: {path}")
	print(f"Risk: {total_risk}")
	print_map(list(path))
	return path

solve_graph((0, 0))
