from typing import Generator
from itertools import pairwise

def load_file_nums() -> Generator:
	with open("input.txt") as f:
		while line := f.readline():
			yield int(line)

data = list(load_file_nums())
num_increasing = sum(1 for _ in filter(
	lambda v: v[1] > v[0], pairwise(
		map(lambda v: sum(v),
			zip(data[:-2], data[1:-1], data[2:])
		)
	)
))
print(num_increasing)
