from typing import Tuple, List, Set

Point = Tuple[int, int]

def load_paper(name: str) -> Tuple[List[Point], List[Tuple[str, int]]]:
	with open(f"{name}.txt") as f:
		points_list = []
		while (line := f.readline()) and "," in line:
			split_i = line.index(",")
			points_list.append((int(line[:split_i]), int(line[split_i + 1:])))
		folds_list = []
		while line := f.readline():
			split_i = line.rindex("=")
			folds_list.append((line[split_i-1:split_i], int(line[split_i+1:])))
		return points_list, folds_list

points, folds = load_paper("input")
width = max(map(lambda p: p[0], points))
height = max(map(lambda p: p[1], points))

def print_paper():
	hashed_points = set(points)
	for y in range(height):
		for x in range(width):
			if (x, y) in hashed_points:
				print("#", end="")
			else:
				print(".", end="")
		print()
	print(f"{len(hashed_points)} points")

def vertical_fold(fold_pos: int):
	for i, point in enumerate(points):
		if (y_diff := point[1] - fold_pos) > 0:
			points[i] = (point[0], fold_pos - y_diff)
	global height
	height //= 2

def horizontal_fold(fold_pos: int):
	for i, point in enumerate(points):
		if (x_diff := point[0] - fold_pos) > 0:
			points[i] = (fold_pos - x_diff, point[1])
	global width
	width //= 2

for fold in folds:
	if fold[0] == "x":
		horizontal_fold(fold[1])
	else:
		vertical_fold(fold[1])
	break

print("Final paper:")
print_paper()
print()
