from typing import Generator

def load_instructions() -> Generator:
	with open("input.txt") as f:
		while line := f.readline():
			line = line.split()
			yield line[0], int(line[1])

x = 0
y = 0

for cmd, val in load_instructions():
	match cmd:
		case "forward":
			x += val
		case "up":
			y = max(0, y - val)
		case "down":
			y += val

print(x * y)
