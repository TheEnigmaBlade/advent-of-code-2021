from io import StringIO
from math import prod
from typing import NamedTuple

def load_message(name: str) -> str:
	with open(f"{name}.txt") as f:
		original_str = f.readline().strip()
		return bin(int(original_str, 16))[2:].zfill(len(original_str) * 4)

message = load_message("input")
print(message)
message_read = StringIO(message)

Packet = NamedTuple("Packet", version=int, type_id=int)

class LiteralPacket(Packet):
	value: int
	
class OperatorPacket(Packet):
	length_type: int 			# 0 = 15-bit length of bits, 1 = 11-bit # packets
	length: int
	subpackets: list[Packet]

def parse_packet(msg: StringIO) -> Packet:
	version = int(msg.read(3), 2)
	type_id = int(msg.read(3), 2)
	
	# Literal
	if type_id == 4:
		packet = LiteralPacket(version, type_id)
		packet.value = parse_literal_value(msg)
	# Operator
	else:
		packet = OperatorPacket(version, type_id)
		packet.length_type = int(msg.read(1), 2)
		# 15-bit length
		if packet.length_type == 0:
			packet.length = int(msg.read(15), 2)
			packet.subpackets = parse_subpacket_length(msg, packet.length)
		# 11-bit packet count
		else:
			packet.length = int(msg.read(11), 2)
			packet.subpackets = parse_subpacket_count(msg, packet.length)
				
	return packet

def parse_literal_value(msg: StringIO) -> int:
	literal = ""
	while (part := msg.read(5))[0] == "1":
		literal += part[1:]
	literal += part[1:]
	return int(literal, 2)

def parse_subpacket_length(msg: StringIO, length: int) -> list[Packet]:
	subpackets = []
	new_packet_str = StringIO(msg.read(length))
	while new_packet_str.tell() < length:
		subpackets.append(parse_packet(new_packet_str))
	return subpackets

def parse_subpacket_count(msg: StringIO, count: int) -> list[Packet]:
	return [parse_packet(msg) for _ in range(count)]

def print_packet(packet: Packet):
	if isinstance(packet, LiteralPacket):
		print(packet)
		print(f"  Value={packet.value}")
	elif isinstance(packet, OperatorPacket):
		print(packet)
		print(f"  Type={ {0: 'sum', 1: 'product', 2: 'minimum', 3: 'maximum', 5: 'greater than', 6: 'less than', 7: 'equal to'}[packet.type_id] }")
		print(f"  Length type={packet.length_type}")
		if packet.length_type == 0:
			print(f"  Length={packet.length}")
		else:
			print(f"  Packet count={packet.length}")
		for sub_packet in packet.subpackets:
			print_packet(sub_packet)

root_packet = parse_packet(message_read)
print_packet(root_packet)

def solve_packet(packet: Packet) -> int:
	match packet.type_id:
		case 0:		# Sum
			return sum(map(solve_packet, packet.subpackets))
		case 1:  	# Product
			return prod(map(solve_packet, packet.subpackets))
		case 2:  	# Minimum
			return min(map(solve_packet, packet.subpackets))
		case 3:  	# Maximum
			return max(map(solve_packet, packet.subpackets))
		case 4:  	# Literal
			return packet.value
		case 5:  	# Greater than
			return 1 if solve_packet(packet.subpackets[0]) > solve_packet(packet.subpackets[1]) else 0
		case 6:  	# Less than
			return 1 if solve_packet(packet.subpackets[0]) < solve_packet(packet.subpackets[1]) else 0
		case 7:  	# Equal to
			return 1 if solve_packet(packet.subpackets[0]) == solve_packet(packet.subpackets[1]) else 0
		case _:
			raise ValueError(f"Unknown packet type {packet.type_id}")
	
solution = solve_packet(root_packet)
print(f"Solution: {solution}")
