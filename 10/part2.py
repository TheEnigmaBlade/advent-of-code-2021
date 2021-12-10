from collections import deque
from functools import reduce
from typing import List, Tuple, Deque, Union, Iterable

def load_nav(name: str):
	with open(f"{name}.txt") as f:
		return [list(iter(line.strip())) for line in f.readlines()]

nav_lines = load_nav("input")

token_pair_map = {
	")": "(",
	"]": "[",
	"}": "{",
	">": "<",
}

def find_syntax_error_index(tokens: List[str]) -> Tuple[int, Union[str, Deque[str]]]:
	chunk_stack = deque()
	for i, token in enumerate(tokens):
		match token:
			case "(" | "[" | "{" | "<":
				chunk_stack.append(token)
			case ")" | "]" | "}" | ">":
				if chunk_stack.pop() != token_pair_map[token]:
					#print(f"Syntax error at index {i}, token {token}")
					return i, token
				
	return -1, chunk_stack

token_score_map = {
	"(": 1,
	"[": 2,
	"{": 3,
	"<": 4,
}

def calc_completion_score(remaining_tokens: Iterable[str]) -> int:
	return reduce(lambda total, val: total * 5 + val,
		map(token_score_map.get, reversed(remaining_tokens))
	)

completion_scores = []

for nav_line in nav_lines:
	error_i, error_token = find_syntax_error_index(nav_line)
	if error_i < 0:
		completion_scores.append(calc_completion_score(error_token))

completion_scores = list(sorted(completion_scores))
middle_score = completion_scores[len(completion_scores) // 2]

print(f"Middle score: {middle_score}")
