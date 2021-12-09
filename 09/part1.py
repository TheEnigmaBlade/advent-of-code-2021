from typing import Iterable

def load_map(name: str):
	with open(f"{name}.txt") as f:
		return [list(map(int, line.strip())) for line in f.readlines()]

map_data = load_map("input")
row_len = len(map_data[0])
col_len = len(map_data)

def get_neighbors(row_i, col_i) -> Iterable[int]:
	return filter(lambda x: x >= 0, [
		map_data[row_i - 1][col_i] if row_i > 0 else -1,			# Up
		map_data[row_i + 1][col_i] if row_i < col_len - 1 else -1,	# Down
		map_data[row_i][col_i - 1] if col_i > 0 else -1,			# Left
		map_data[row_i][col_i + 1] if col_i < row_len - 1 else -1,  # Right
	])

num_low_points = 0
risk_level = 0

for row in range(col_len):
	for col in range(row_len):
		current_val = map_data[row][col]
		# Check if low point
		if len(list(filter(lambda x: current_val >= x, get_neighbors(row, col)))) == 0:
			#print(f"[{row}, {col}] = {current_val}")
			num_low_points += 1
			risk_level += current_val + 1

print(f"Num low points: {num_low_points}")
print(f"Risk level:     {risk_level}")
