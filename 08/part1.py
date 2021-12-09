from typing import List, Tuple, Set, Dict, Iterable

DisplayInput = Tuple[List[str], List[str]]

def sort_string(s: str) -> str:
	return "".join(sorted(s))

def load_data(name: str) -> List[DisplayInput]:
	with open(f"{name}.txt") as f:
		return [tuple(map(lambda side: list(map(lambda s: sort_string(s), side.strip().split(" "))), line.split("|"))) for line in f.readlines()]

def train_segment_map(train_data: List[str]) -> Dict[str, str]:
	# Train translation mapping
	train_data = sorted(train_data, key=len)
	print(f"Train data: {train_data}")
	
	def gen_seg_char():
		return iter(chr(97 + c) for c in range(7))
	
	segment_map: Dict[str, Set[str]] = {c: set(gen_seg_char()) for c in gen_seg_char()}
	
	def update_segment_map(known_segments: Iterable[str], origin_segments: Iterable[str]):
		for s in known_segments:
			segment_map[s].intersection_update(origin_segments)
		for s in set(known_segments).symmetric_difference(segment_map.keys()):
			segment_map[s].difference_update(origin_segments)
	
	segment_collections = {x: set(gen_seg_char()) for x in (5, 6)}
	for segments in train_data:
		match len(segments):
			case 2:
				update_segment_map(segments, ("c", "f"))
			case 3:
				update_segment_map(segments, ("a", "c", "f"))
			case 4:
				update_segment_map(segments, ("b", "d", "c", "f"))
			case 5 | 6:
				segment_collections[len(segments)].intersection_update(segments)
	
	update_segment_map(segment_collections[5], ("a", "d", "g"))
	update_segment_map(segment_collections[6], ("a", "b", "f", "g"))
	return {k: v.pop() for k, v in segment_map.items()}

digit_table = {
	"abcefg":	0,
	"cf":		1,
	"acdeg":	2,
	"acdfg":	3,
	"bcdf":		4,
	"abdfg":	5,
	"abdefg":	6,
	"acf":		7,
	"abcdefg":	8,
	"abcdfg":	9,
}

def solve_display(display_input: DisplayInput) -> List[int]:
	segment_map = train_segment_map(display_input[0])
	print(f"Segment map: {segment_map}")
	segment_trans = str.maketrans(segment_map)
	
	# Translate digits
	display_data = display_input[1]
	print(f"Four digits: {display_data}")
	translated_digits = []
	for digit in display_data:
		digit = sort_string(digit.translate(segment_trans))
		translated_digits.append(digit_table[digit])
	
	return translated_digits

total_digits = 0
target_digits = {1, 4, 7, 8}

for di in load_data("input"):
	solution = solve_display(di)
	print(f"Solution: {solution}")
	total_digits += len([d for d in solution if d in target_digits])
	
print(f"\nTotal target digits: {total_digits}")
