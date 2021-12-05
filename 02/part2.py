from typing import Generator

def load_instructions(name: str) -> Generator:
	with open(f"{name}.txt") as f:
		while line := f.readline():
			line = line.split()
			yield line[0], int(line[1])

x = 0
y = 0
aim = 0

for cmd, val in load_instructions("input"):
	match cmd:
		case "forward":
			x += val
			y += max(0, val * aim)
		case "up":
			aim -= val
		case "down":
			aim += val

print(x * y)
