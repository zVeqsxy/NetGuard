from scapy.all import sniff 

class PacketSniffing:
	def __init__(self):
		pass
	
	def capturePackets(self, interfaces, filter):
		packets = []
		for interface in interfaces:
			packets.append(sniff(filter=filter, count=10, iface=interface, timeout=3))
		
		dissaembled_packets = self.disassemble(packets)
		return dissaembled_packets

	def disassemble(self, packets):
		data = {}
		# Process each captured packet
		for i, packet in enumerate(packets):
			# Print the source and destination IP addresses
			data["source_ip"] = packet[i][0][1].src
			data["destination_ip"] = packet[i][0][1].dst
			data["protocol"] = packet[i][0][1].proto
			data["length"] = len(packet[i])
			data["packet"] = packet[i].show()
			data["summary"] = packet[i].summary()

			print(f"Source IP: {packet[0][1].src}")
			print(f"Destination IP: {packet[0][1].dst}")

			# Print the packet's protocol
			print(f"Protocol: {packet[0][1].proto}")

			# Print the packet's length
			print(f"Length: {len(packet)}")

			# Print the packet
			print(packet.show())

			# Print a separator
			print("-" * 80)

			# Print the packet's summary
			print(packet.summary())

		return data