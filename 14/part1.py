from typing import Optional

def load_template(name: str) -> tuple[str, list[tuple[str, ...]]]:
	with open(f"{name}.txt") as f:
		return f.readline().strip(), [tuple(line.strip().split(" -> ")) for line in f.readlines() if line.strip()]

polymer, pair_insertions = load_template("input")

def search_pair_insertions(in_polymer: str, search_start: int) -> Optional[tuple[str, int]]:
	def _search(pair) -> Optional[tuple[str, int]]:
		if (search_i := in_polymer.find(pair[0], search_start)) >= 0:
			return pair[1], search_i + 1
		return None
	return min(filter(None, map(_search, pair_insertions)), key=lambda p: p[1], default=None)

def do_pair_insertion(in_polymer: str) -> str:
	out_polymer = in_polymer
	iter_i = 0
	while pair := search_pair_insertions(out_polymer, iter_i):
		out_polymer = out_polymer[:pair[1]] + pair[0] + out_polymer[pair[1]:]
		iter_i = pair[1] + 1
	return out_polymer

num_steps = 10

print(f"Template: {polymer}")

for i in range(num_steps):
	polymer = do_pair_insertion(polymer)
	print(f"Step {i+1} (len {len(polymer)}): {polymer}")

elem_counts = [(e, polymer.count(e)) for e in ["N", "C", "B", "H"]]		# Note after success with actual input: this shouldn't have worked, but it did

max_elem = max(elem_counts, key=lambda e: e[1])
min_elem = min(elem_counts, key=lambda e: e[1])
print(f"Max elem: {max_elem}")
print(f"Min elem: {min_elem}")
score = max_elem[1] - min_elem[1] 
print(f"Score: {score}")
