from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, List, Iterator
import re

@dataclass
class Line:
	x1: int; y1: int
	x2: int; y2: int
	
	def iter_point(self) -> Iterator[Tuple[int, int]]:
		# Horizontal line
		if self.y1 == self.y2:
			for x in range(min(self.x1, self.x2), max(self.x1, self.x2) + 1):
				yield x, self.y1
		# Vertical line
		elif self.x1 == self.x2:
			for y in range(min(self.y1, self.y2), max(self.y1, self.y2) + 1):
				yield self.x1, y

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
