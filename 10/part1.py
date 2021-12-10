from collections import deque
from pprint import pprint
from typing import List, Tuple

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

def find_syntax_error_index(tokens: List[str]) -> Tuple[int, str]:
	chunk_stack = deque()
	for i, token in enumerate(tokens):
		match token:
			case "(" | "[" | "{" | "<":
				chunk_stack.append(token)
			case ")" | "]" | "}" | ">":
				if chunk_stack.pop() != token_pair_map[token]:
					print(f"Syntax error at index {i}, token {token}")
					return i, token
				
	return -1, ""

token_score_map = {
	")": 3,
	"]": 57,
	"}": 1197,
	">": 25137,
}

syntax_error_score = 0

for nav_line in nav_lines:
	error_i, error_token = find_syntax_error_index(nav_line)
	if error_i >= 0:
		syntax_error_score += token_score_map[error_token]

print(f"Syntax error score: {syntax_error_score}")
