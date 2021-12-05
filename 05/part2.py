from collections import defaultdict
from dataclasses import dataclass
from itertools import repeat
from typing import Tuple, List, Iterator
import re

@dataclass
class Line:
	x1: int; y1: int
	x2: int; y2: int
	
	def iter_point(self) -> Iterator[Tuple[int, int]]:
		step_x = -1 if self.x2 < self.x1 else 1
		step_y = -1 if self.y2 < self.y1 else 1
		return zip(
			range(self.x1, self.x2 + step_x, step_x) if self.x1 != self.x2 else repeat(self.x1),	# x
			range(self.y1, self.y2 + step_y, step_y) if self.y1 != self.y2 else repeat(self.y1)		# y
		)

def load_map(name: str) -> List[Line]:
	line_extract_re = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
	
	with open(f"{name}.txt") as f:
		lines = []
		while line := f.readline():
			if match := line_extract_re.match(line):
				lines.append(Line(*map(int, match.groups())))
		return lines

vents = load_map("input")

from pprint import pprint

point_accum = defaultdict(int)
for vent in vents:
	#pprint(vent)
	for point in vent.iter_point():
		#print(point)
		point_accum[point] = point_accum[point] + 1

num_overlap = len(list(filter(lambda c: c > 1, point_accum.values())))
print(f"{num_overlap} overlapping points")
