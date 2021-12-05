from typing import List, Tuple, Set, Iterable, Iterator

class Board:
	def __init__(self, init_vals: Iterable[int]):
		self.vals: List[int] = list(init_vals)
		self.marked: Set[int] = set()
	
	def add_row(self, row: Iterable[int]):
		self.vals.extend(row)
	
	def is_winner(self) -> bool:
		for i in range(0, 5):
			if self.is_winning_row(i * 5) or self.is_winning_col(i):
				return True
		return False
	
	def is_winning_row(self, start_idx) -> bool:
		idx = list(range(start_idx, start_idx+5))
		return all(map(lambda i: i in self.marked, idx))
	
	def is_winning_col(self, start_idx) -> bool:
		idx = list(range(start_idx, 25, 5))
		return all(map(lambda i: i in self.marked, idx))
	
	def mark_val(self, val):
		try:
			i = self.vals.index(val)
			self.marked.add(i)
		except ValueError:
			pass
	
	def iter_unmarked(self) -> Iterator[int]:
		#return map(self.vals.__getitem__, filterfalse(self.marked.__contains__, map(self.vals.index, self.vals)))
		return map(lambda e: e[1], filter(lambda e: e[0] not in self.marked, enumerate(self.vals)))
	
	def __repr__(self):
		vstr = ", ".join(map(lambda e: f"*{e[1]}*" if e[0] in self.marked else str(e[1]), enumerate(self.vals)))
		return f"[{vstr}] | {self.marked}"

def load_game(name: str) -> Tuple[List[int], List[Board]]:
	with open(f"{name}.txt") as f:
		line = f.readline()
		picks = list(map(int, line.split(",")))
		
		boards = []
		while line := f.readline():
			line = line.strip()
			if not len(line):
				continue
			
			board = Board(map(int, line.strip().split()))
			for _ in range(4):
				board.add_row(map(int, f.readline().strip().split()))
			boards.append(board)
		
		return picks, boards

def main():
	picks, boards = load_game("input")
	
	for pick in picks:
		print(f"-- Pick {pick}")
		for board in list(boards):
			board.mark_val(pick)
			#print(board)
			if board.is_winner():
				if len(boards) == 1:
					# Calculate result
					print(board)
					print(list(board.iter_unmarked()))
					print(sum(board.iter_unmarked()))
					score = sum(board.iter_unmarked()) * pick
					print(f"Score = {score}")
					return
				else:
					print("Removing board")
					boards.remove(board)

main()
