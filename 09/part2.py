from typing import Iterable, Tuple
from functools import reduce
import operator
from pprint import pprint
import colorama
from colorama import Fore, Back, Style
colorama.init()

def load_map(name: str):
	with open(f"{name}.txt") as f:
		return [list(map(int, line.strip())) for line in f.readlines()]

map_data = load_map("input")
row_len = len(map_data[0])
col_len = len(map_data)

def print_map(basins, largest_keys: Iterable[Tuple[int, int]]):
	for row_i in range(col_len):
		for col_i in range(row_len):
			key = (row_i, col_i)
			val = map_data[row_i][col_i]
			
			in_basin = False
			basin_core = None
			for basin_key, basin in basins.items():
				if key in basin:
					in_basin = True
					basin_core = basin_key
					break
			
			if key in basins.keys():
				color = Back.RED if key in largest_keys else Back.CYAN
				print(f"{color}{val}{Style.RESET_ALL} ", end="")
			elif in_basin:
				color = Fore.RED if basin_core in largest_keys else Fore.CYAN
				print(f"{color}{val}{Style.RESET_ALL} ", end="")
			else:
				print(f"{Fore.LIGHTBLACK_EX}{val}{Style.RESET_ALL} ", end="")
		print()
				

def get_neighbors(row_i, col_i) -> Iterable[int]:
	return filter(lambda x: x >= 0, [
		map_data[row_i - 1][col_i] if row_i > 0 else -1,			# Up
		map_data[row_i + 1][col_i] if row_i < col_len - 1 else -1,	# Down
		map_data[row_i][col_i - 1] if col_i > 0 else -1,			# Left
		map_data[row_i][col_i + 1] if col_i < row_len - 1 else -1,  # Right
	])

def get_basin(row_i, col_i, origin_value=-1):
	# Terminate if out of bounds
	if row_i < 0 or row_i >= col_len or col_i < 0 or col_i >= row_len:
		return []
	val = map_data[row_i][col_i]
	# Terminate on leaf not meeting basin criteria
	if (origin_value >= 0 and val <= origin_value) or val == 9:
		return []
	# Determine basin from this point outwards (naive recursion; not optimized)
	basin_points = {(row_i, col_i)}
	basin_points.update(get_basin(row_i - 1, col_i, val))
	basin_points.update(get_basin(row_i + 1, col_i, val))
	basin_points.update(get_basin(row_i, col_i - 1, val))
	basin_points.update(get_basin(row_i, col_i + 1, val))
	return basin_points

basins = dict()
for row in range(col_len):
	for col in range(row_len):
		current_val = map_data[row][col]
		# Check if low point
		if len(list(filter(lambda x: current_val >= x, get_neighbors(row, col)))) == 0:
			basins[(row, col)] = get_basin(row, col)

print(f"Num basins: {len(basins)}")
top_basins = list(sorted(map(lambda i: (i[0], len(i[1])), basins.items()), key=lambda v: v[1], reverse=True))[:3]
#top_basins = list(sorted(map(len, basins.values()), reverse=True))[:3]
for core, length in top_basins:
	print(f"Core {core} = {length}")
result = reduce(operator.mul, map(lambda v: v[1], top_basins))
print(f"Result:     {result}")

print()
print_map(basins, list(map(lambda v: v[0], top_basins)))
