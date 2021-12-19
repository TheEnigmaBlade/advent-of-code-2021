from io import StringIO
from itertools import permutations
from math import floor, ceil
from random import randint
from copy import deepcopy
from typing import Optional

class SnailfishNum:
	_id: int
	value: Optional[int]
	left: Optional["SnailfishNum"]
	right: Optional["SnailfishNum"]
	parent: Optional["SnailfishNum"]
	
	def __init__(self, value=None, left=None, right=None):
		self._id = randint(0, 99999)
		self.value = value
		self.left = left
		if self.left:
			self.left.parent = self
		self.right = right
		if self.right:
			self.right.parent = self
		self.parent = None
	
	def __eq__(self, other: "SnailfishNum"):
		return self._id == other._id
	
	@property
	def depth(self) -> int:
		return (1 if self.value is None else 0) + max(self.left.depth if self.left else 0, self.right.depth if self.right else 0)
	
	@property
	def inv_depth(self) -> int:
		return 1 + self.parent.inv_depth if self.parent else 1
	
	def replace(self, child_num: "SnailfishNum", replace_num: "SnailfishNum"):
		if self.left == child_num:
			self.replace_left(replace_num)
		elif self.right == child_num:
			self.replace_right(replace_num)
	
	def replace_left(self, replace_num: "SnailfishNum"):
		self.left = replace_num
		self.left.parent = self
	
	def replace_right(self, replace_num: "SnailfishNum"):
		self.right = replace_num
		self.right.parent = self
	
def load_numbers(name: str) -> list[SnailfishNum]:
	def parse_number(num_read: StringIO) -> SnailfishNum:
		if (c := num_read.read(1)).isdigit():
			return SnailfishNum(value=int(c))
		elif c == "[":
			left = parse_number(num_read)
			assert num_read.read(1) == ","
			right = parse_number(num_read)
			assert num_read.read(1) == "]"
			new_num = SnailfishNum(left=left, right=right)
			left.parent = new_num
			right.parent = new_num
			return new_num
	
	with open(f"{name}.txt") as f:
		return [parse_number(StringIO(line.strip())) for line in f.readlines()]
	
def print_num(num: SnailfishNum, end="\n"):
	if num.value is not None:
		return print(f"{num.value}", end=end)
	print("[", end="")
	print_num(num.left, end="")
	print(",", end="")
	print_num(num.right, end="")
	print("]", end=end)

def reduce(num: SnailfishNum) -> SnailfishNum:
	while explode(num) or split(num):
		pass
	return num

def explode(num: SnailfishNum, max_depth=4) -> bool:
	if reduce_pair := _find_leftmost_explode_num(num, max_depth):
		#print(f"Pre explode: {num.depth}")
		#print_num(num)
		#print("Exploding pair: ", end="")
		#print_num(reduce_pair)
		
		# Add left pair to closest left number
		leftmost_num = _search_closest_left(reduce_pair)
		#print(f"Leftmost: {leftmost_num.value if leftmost_num else None}")
		if leftmost_num:
			leftmost_num.value += reduce_pair.left.value
		# Add right pair to closest right number
		rightmost_num = _search_closest_right(reduce_pair)
		#print(f"Rightmost: {rightmost_num.value if rightmost_num else None}")
		if rightmost_num:
			rightmost_num.value += reduce_pair.right.value
		# Replace pair with 0
		reduce_pair.parent.replace(reduce_pair, SnailfishNum(value=0))
		
		#print(f"Post explode: {num.depth}")
		#print_num(num)
		return True
	return False

def _find_leftmost_explode_num(num: SnailfishNum, remaining_depth) -> Optional[SnailfishNum]:
	if not num:
		return None
	if num.depth == 1 and remaining_depth <= 0:
		return num
	return _find_leftmost_explode_num(num.left, remaining_depth - 1) or _find_leftmost_explode_num(num.right, remaining_depth - 1)

def _search_closest_left(num: SnailfishNum, descend=False) -> Optional[SnailfishNum]:
	if descend:
		if num.value is not None:
			return num
		#print(" > ", end="")
		#print_num(num)
		return _search_closest_left(num.right, descend)
	else:
		if not num.parent:
			return None
		if num.parent.left == num:
			#print(" < ", end="")
			#print_num(num.parent)
			return _search_closest_left(num.parent)
		return _search_closest_left(num.parent.left, descend=True)

def _search_closest_right(num: SnailfishNum, descend=False) -> Optional[SnailfishNum]:
	if descend:
		if num.value is not None:
			return num
		#print(" < ", end="")
		#print_num(num)
		return _search_closest_right(num.left, descend)
	else:
		if not num.parent:
			return None
		if num.parent.right == num:
			#print(" > ", end="")
			#print_num(num.parent)
			return _search_closest_right(num.parent)
		return _search_closest_right(num.parent.right, descend=True)

def split(num: SnailfishNum) -> bool:
	if split_pair := _find_leftmost_split_num(num):
		#print(f"Pre split: {num.depth}")
		#print_num(num)
		#print("Splitting num: ", end="")
		#print_num(split_pair)
		
		split_pair.replace_left(SnailfishNum(floor(split_pair.value / 2)))
		split_pair.replace_right(SnailfishNum(ceil(split_pair.value / 2)))
		split_pair.value = None
		
		#print(f"Post split: {num.depth}")
		#print_num(num)
		return True
	return False

def _find_leftmost_split_num(num: SnailfishNum) -> Optional[SnailfishNum]:
	if not num:
		return None
	if num.value and num.value > 9:
		return num
	return _find_leftmost_split_num(num.left) or _find_leftmost_split_num(num.right)

def add(num1: SnailfishNum, num2: SnailfishNum) -> SnailfishNum:
	return reduce(SnailfishNum(left=deepcopy(num1), right=deepcopy(num2)))

def magnitude(num: SnailfishNum) -> int:
	if num.value is not None:
		return num.value
	return magnitude(num.left) * 3 + magnitude(num.right) * 2 

numbers = load_numbers("input")
for n in numbers:
	print_num(n)

count = 1
max_magnitude = 0
for num1, num2 in permutations(numbers, 2):
	print(f"  ", end="")
	print_num(num1)
	print(f"+ ", end="")
	print_num(num2)
	added = add(num1, num2)
	new_mag = magnitude(added)
	print(f"Mag {count}: {new_mag}")
	print()
	count += 1
	max_magnitude = max(max_magnitude, new_mag)

print(f"Max magnitude: {max_magnitude}")
