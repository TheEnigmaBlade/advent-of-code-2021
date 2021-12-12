from typing import Tuple, List, Set
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

def find_paths(routes: Tree, nodes_can_enter: Set[str], current_path: List[str]) -> List[List[str]]:
	if routes.name not in nodes_can_enter:
		return []
	
	current_path.append(routes.name)
	if routes.name == "end":
		return [current_path]
	
	if routes.name.islower():
		nodes_can_enter.remove(routes.name)
	
	all_paths = []
	for child in routes.children:
		all_paths.extend(find_paths(child, set(nodes_can_enter), list(current_path)))
	return all_paths

connection_list = load_connections("input")
route_tree, node_list = gen_route_tree(connection_list)

paths = find_paths(route_tree, node_list, [])
pprint(paths)
print(f"Num paths: {len(paths)}")
