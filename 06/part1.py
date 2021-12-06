from typing import List

def load_fish(name: str) -> List[int]:
	with open(f"{name}.txt") as f:
		return list(map(int, f.readline().strip().split(",")))

fish_list = load_fish("input")
num_days = 80

print(f"Initial: {fish_list}")

for current_day in range(1, num_days+1):
	for fish_i in range(len(fish_list)):
		fish = fish_list[fish_i]
		if fish == 0:
			fish = 6
			fish_list.append(8)
		else:
			fish -= 1
		fish_list[fish_i] = fish
	#print(f"Day {current_day:2}: {fish_list}")
	
print(f"Final: {len(fish_list)} fish")
