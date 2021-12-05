from typing import Generator
from itertools import pairwise

def load_file_nums() -> Generator:
	with open("input.txt") as f:
		while line := f.readline():
			yield int(line)

num_increasing = sum(1 for _ in filter(lambda v: v[1] > v[0], pairwise(load_file_nums())))
print(num_increasing)
