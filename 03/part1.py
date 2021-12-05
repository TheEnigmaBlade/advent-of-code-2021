from typing import Generator

def load_report(name: str) -> Generator:
	with open(f"{name}.txt") as f:
		while line := f.readline():
			yield line.strip()

gamma = ""
epsilon = ""

for bits in zip(*load_report("input")):
	num_0 = 0
	num_1 = 0
	for bit in bits:
		if bit == "0":
			num_0 += 1
		else:
			num_1 += 1

	#print(f"0 = {num_0}; 1 = {num_1}")	

	if num_0 > num_1:
		gamma += "0"
		epsilon += "1"
	else:
		gamma += "1"
		epsilon += "0"

print(f"gamma = {gamma}")
print(f"epsilon = {epsilon}")

gamma = int(gamma, 2)
epsilon = int(epsilon, 2)
print(f"power = {gamma * epsilon}")
