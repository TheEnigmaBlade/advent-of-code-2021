from itertools import product
from pprint import pprint

def load_octo(name: str):
	with open(f"{name}.txt") as f:
		return [list(map(int, line.strip())) for line in f.readlines()]

octo_grid = load_octo("input")
width = 10
height = 10

def step() -> int:
	indecies_flashing = set()
	
	def update_flash(core_x: int, core_y: int):
		if core_x < 0 or core_x >= width or core_y < 0 or core_y >= height:
			return
		if (core_x, core_y) in indecies_flashing:
			return
		# Increment energy (for both the standard increment and flash increment)
		octo_grid[core_y][core_x] += 1
		# Cascade flashing
		if octo_grid[core_y][core_x] > 9:
			indecies_flashing.add((core_x, core_y))
			update_flash(core_x - 1, core_y - 1)
			update_flash(core_x - 1, core_y)
			update_flash(core_x - 1, core_y + 1)
			update_flash(core_x, core_y - 1)
			update_flash(core_x, core_y)
			update_flash(core_x, core_y + 1)
			update_flash(core_x + 1, core_y - 1)
			update_flash(core_x + 1, core_y)
			update_flash(core_x + 1, core_y + 1)
	
	for x, y in product(range(width), range(height)):
		update_flash(x, y)
	
	# Reset flashing
	for x, y in indecies_flashing:
		octo_grid[y][x] = 0
	return len(indecies_flashing)


num_steps = 100
total_flashes = 0

pprint(octo_grid)
print()

for i in range(num_steps):
	num_flashes = step()
	print(f"Step {i}: {num_flashes} flashes")
	pprint(octo_grid)
	print()
	total_flashes += num_flashes
	

print(f"Total flashes: {total_flashes}")
