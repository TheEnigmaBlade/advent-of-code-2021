from io import StringIO
from typing import NamedTuple

def load_message(name: str) -> str:
	with open(f"{name}.txt") as f:
		binary = bin(int(f.readline().strip(), 16))[2:]
		if len(binary) % 4 == 0:
			return binary
		return binary.zfill((len(binary) // 4 + 1) * 4)

message = load_message("input")
print(message)
message_read = StringIO(message)

Packet = NamedTuple("Packet", version=int, type_id=int)

class LiteralPacket(Packet):
	values: list[int]
	
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
		packet.values = parse_literal_value(msg)
	# Operator
	else:
		packet = OperatorPacket(version, type_id)
		packet.length_type = int(msg.read(1), 2)
		# 15-bit length
		if packet.length_type == 0:
			len_str = msg.read(15)
			packet.length = int(len_str, 2)
			new_packet_str = StringIO(msg.read(packet.length))
			packet.subpackets = []
			while new_packet_str.tell() < len(new_packet_str.getvalue()):
				packet.subpackets.append(parse_packet(new_packet_str))
		
		# 11-bit packet count
		else:
			packet.length = int(msg.read(11), 2)
			packet.subpackets = [parse_packet(msg) for _ in range(packet.length)]
				
	return packet

def parse_literal_value(msg: StringIO) -> int:
	literal = ""
	while (part := msg.read(5))[0] == "1":
		literal += part[1:]
	literal += part[1:]
	return int(literal, 2)

def print_packet(packet: Packet):
	if isinstance(packet, LiteralPacket):
		print(packet)
		print(f"  Values={packet.values}")
	elif isinstance(packet, OperatorPacket):
		print(packet)
		print(f"  Length type={packet.length_type}")
		if packet.length_type == 0:
			print(f"  Length={packet.length}")
		else:
			print(f"  Packet count={packet.length}")
		for sub_packet in packet.subpackets:
			print_packet(sub_packet)

root_packet = parse_packet(message_read)
print_packet(root_packet)

def get_version_total(packet: Packet) -> int:
	# Literal
	if packet.type_id == 4:
		return packet.version
	# Operator
	else:
		return packet.version + sum(map(get_version_total, packet.subpackets))

version_total = get_version_total(root_packet)
print(f"\nVersion total: {version_total}")
