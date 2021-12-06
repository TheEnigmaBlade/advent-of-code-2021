from typing import Dict

def load_fish(name: str) -> Dict[int, int]:
	with open(f"{name}.txt") as f:
		buckets = {k: 0 for k in range(9)}
		for x in map(int, f.readline().strip().split(",")):
			buckets[x] += 1
		return buckets

fish_buckets = load_fish("input")
num_days = 256

print(f"Initial: {fish_buckets}")

for current_day in range(1, num_days + 1):
	fish_count_0 = fish_buckets[0]
	# Update normal fish, move age down by 1
	for fish_age in range(1, 9):
		fish_count = fish_buckets[fish_age]
		fish_buckets[fish_age - 1] = fish_count
	# Spawn new fish
	fish_buckets[8] = fish_count_0
	# Reset old fish
	fish_buckets[6] += fish_count_0

print(f"Final: {sum(fish_buckets.values())} fish")
