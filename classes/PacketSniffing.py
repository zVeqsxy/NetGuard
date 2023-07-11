class PacketSniffing:
	def __init__(self):
		pass
	
	def sniffing(self):
		pass
		
	def disassemble(self, packets):
		# Process each captured packet
		for packet in packets:
			# Print the source and destination IP addresses
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