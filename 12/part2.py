from typing import Tuple, List, Set, Dict
from pprint import pprint

def load_connections(name: str) -> List[Tuple[str, str]]:
	with open(f"{name}.txt") as f:
		# noinspection PyTypeChecker
		return [tuple(line.strip().split("-")) for line in f.readlines()]

class Tree:
	def __init__(self, name: str):
		self.name = name
		self.children = set()
	
def gen_route_tree(connections: List[Tuple[str, str]]) -> Tuple[Tree, Set[str]]:
	root = Tree("start")
	node_map = {root.name: root}
	
	for connection in connections:
		if not (node1 := node_map.get(connection[0])):
			node1 = node_map.setdefault(connection[0], Tree(connection[0]))
		if not (node2 := node_map.get(connection[1])):
			node2 = node_map.setdefault(connection[1], Tree(connection[1]))
		
		node1.children.add(node2)
		node2.children.add(node1)
	
	return root, set(node_map.keys())

def find_paths(routes: Tree, nodes_enter_remaining: Set[str], current_path: List[str], entered_twice=False) -> Set[str]:
	if routes.name not in nodes_enter_remaining:
		return set()
	
	current_path.append(routes.name)
	if routes.name == "end":
		return {",".join(current_path)}
	
	# Iterating twice is a naive approach, but set eliminates identical paths
	all_paths = set()
	# If a lower case room has not been entered twice, iterate before removal of current node
	if not entered_twice and routes.name.islower() and routes.name != "start":
		for child in routes.children:
			all_paths |= find_paths(child, set(nodes_enter_remaining), list(current_path), True)
	# Remove current node and iterate again
	if routes.name.islower():
		nodes_enter_remaining.remove(routes.name)
	for child in routes.children:
		all_paths |= find_paths(child, set(nodes_enter_remaining), list(current_path), entered_twice)
		
	return all_paths

connection_list = load_connections("input")
route_tree, node_list = gen_route_tree(connection_list)

paths = find_paths(route_tree, node_list, [])
pprint(paths)
print(f"Num paths: {len(paths)}")
