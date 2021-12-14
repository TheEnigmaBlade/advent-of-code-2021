from collections import defaultdict
from itertools import pairwise
from pprint import pprint

def load_template(name: str) -> tuple[str, dict[str, str]]:
	with open(f"{name}.txt") as f:
		return f.readline().strip(), {val[0]: val[1] for val in map(lambda line: line.strip().split(" -> "), filter(lambda line: line.strip() != "", f.readlines()))}

polymer, pair_insertions = load_template("input")
print(f"Starting polymer: {polymer}")
num_steps = 40

# Create initial pair count dict
pairs: defaultdict[str, int] = defaultdict(int)
for p in pairwise(polymer):
	pairs["".join(p)] += 1
	
# Apply pair insertions
for i in range(num_steps):
	new_pairs = defaultdict(int)
	for pair_key, pair_count in list(filter(lambda p: p[1] > 0, pairs.items())):
		new_pairs[pair_key[0] + pair_insertions[pair_key]] += pair_count
		new_pairs[pair_insertions[pair_key] + pair_key[1]] += pair_count
	pairs = new_pairs

# Count elements
elem_counts = defaultdict(int)
for pair in pairs:
	elem_counts[pair[0]] += pairs[pair]
	elem_counts[pair[1]] += pairs[pair]
# All counts are doubled, and the first and last elements in the original polymer are off by one (only included in a single pair)
for elem in elem_counts:
	elem_counts[elem] //= 2
elem_counts[polymer[0]] += 1
elem_counts[polymer[-1]] += 1

max_elem = max(elem_counts.items(), key=lambda e: e[1])
min_elem = min(elem_counts.items(), key=lambda e: e[1])
print(f"Max elem: {max_elem}")
print(f"Min elem: {min_elem}")
score = max_elem[1] - min_elem[1]
print(f"Score: {score}")
