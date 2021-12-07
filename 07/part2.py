from typing import List
import math

def load_positions(name: str) -> List[int]:
	with open(f"{name}.txt") as f:
		return list(map(int, f.readline().strip().split(",")))

initial_positions = load_positions("input")
min_pos = 1
max_pos = max(initial_positions)

def fuel_cost(target_pos: int) -> int:
	cost = 0
	for pos in initial_positions:
		pos_cost = abs(pos - target_pos) 
		cost += int(pos_cost * (pos_cost + 1) / 2)
	return cost

best_cost = math.inf
best_pos = 0
for pos in range(min_pos, max_pos):
	if (cost := fuel_cost(pos)) < best_cost:
		best_cost = cost
		best_pos = pos
print(f"Best cost at position {best_pos}: {best_cost}")
