from typing import Generator

def load_report(name: str) -> Generator:
	with open(f"{name}.txt") as f:
		while line := f.readline():
			yield line.strip()

oxygen_data = list(load_report("input"))
co2_data = list(oxygen_data)

def find_value(data, co2=False):
	for i in range(len(data[0])):
		num_0 = 0
		num_1 = 0
		for bit in map(lambda d: d[i], data):
			if bit == "0":
				num_0 += 1
			else:
				num_1 += 1
			
		digit = "0" if (num_0 > num_1 and not co2) or (num_0 <= num_1 and co2) else "1"
		data = list(filter(lambda d: d[i] == digit, data))
		if len(data) == 1:
			break
	return int(data[0], 2)

oxygen_val = find_value(oxygen_data)
co2_val = find_value(oxygen_data, True)
print(f"Oxygen = {oxygen_val}")
print(f"CO2    = {co2_val}")
print(f"Life support = {oxygen_val * co2_val}")
