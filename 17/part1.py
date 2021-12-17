import re
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from typing import NamedTuple

class BoundBox(NamedTuple):
	x1: int
	x2: int
	y1: int
	y2: int
	
	def contains(self, x: int, y: int) -> bool:
		return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
	
	def past(self, x: int, y: int) -> bool:
		return y < self.y1 or x > self.x2

def load_target(name: str) -> BoundBox:
	with open(f"{name}.txt") as f:
		if match := re.search(f"x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", f.readline()):
			return BoundBox(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))
		raise ValueError("Bad file")

target = load_target("input")
print(target)

def solve_trajectory(start_velocity: tuple[int, int]) -> tuple[bool, tuple[int, int], int]:
	x = 0
	y = 0
	y_max = 0
	vx, vy = start_velocity
	
	while not target.past(x, y):
		x += vx
		y += vy
		if y > y_max:
			y_max = y
		
		if target.contains(x, y):
			return True, start_velocity, y_max 
		
		if vx > 0:
			vx -= 1
		vy -= 1
	
	return False, start_velocity, y_max

with ThreadPoolExecutor(max_workers=1) as ex:
	vx_min = 1
	vx_max = 100
	vy_min = 0
	vy_max = 300
	
	successes = []
	for vy in range(vy_min, vy_max+1):
		results = ex.map(solve_trajectory, [(vx, vy) for vx in range(vx_min, vx_max+1)])
		for result in results:
			if result[0]:
				#print(f"Success found: {result[1]}, max height {result[2]}")
				successes.append(result)
	
	print(f"{len(successes)} successes")
	max_y = max(map(lambda s: s[2], successes))
	print(f"Max y position reached: {max_y}")
