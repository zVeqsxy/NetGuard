from scapy.arch.windows import get_windows_if_list
from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import ARP
from scapy.sendrecv import sr1, srp
from scapy.all import sniff
from tabulate import tabulate
from tqdm import tqdm
import threading
import socket
from getmac import get_mac_address

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from classes.MySQL import MySqlCommands
mysql = MySqlCommands()

from lib.menu import active_addresses_label

class IPScanner:
	def __init__(self):
		# self.local_ip = socket.gethostbyname(socket.gethostname())  # get local ip with socket
		# self.local_ip = "local-ip"  # local ip without the last octet (example: 192.168.1.13 = 192.168.1.)
		self.local_ip = "192.168.2."
		self.start_ip = 1
		self.end_ip = 254
		self.responsive_address = []
		self.lock = threading.Lock()  # By using the lock in this scenario, we ensure that only one thread can access the responsive_address list at a time, preventing any conflicts or data corruption

	def ping(self, target_ip):
		# Create the ICMP echo request packet
		icmp_packet = IP(dst=target_ip) / ICMP()

		# Send the ICMP echo request packet and receive the response
		response = sr1(icmp_packet, timeout=1, verbose=False)

		if response:
			with self.lock:
				ip = response.src
				mac = get_mac_address(ip=ip)
				if mac is None:
					print(f"\nNo MAC-address found for this IP: {ip}")
					return
				self.responsive_address.append(ip + "|" + mac)

	def displayActiveAddress(self):
		data = []
		index_values = []
		ip_addr = []
		mac_addr = []

		for address in self.responsive_address:
			ip, mac = address.split("|")
			ip_addr.append(ip)
			mac_addr.append(mac)

		names = mysql.getNames(mac_addr)
		if names:
			for name in names:
				data.append([name[0], name[1], name[2], name[3], name[4]])
				index_values.append(name[0])
		else:
			for ip, mac in zip(ip_addr, mac_addr):
				data.append(["", "", "", ip, mac])

		headers = ["First Name", "Last Name", "Description", "IP-address", "MAC-address"]
		table = tabulate(data, headers=headers, tablefmt="fancy_grid", showindex="never")

		print(active_addresses_label)
		print(table)

	def startPing(self):
		threads = []
		for i in range(self.start_ip, self.end_ip + 1):
			target_ip = self.local_ip + str(i)

			t = threading.Thread(target=self.ping, args=(target_ip,))
			threads.append(t)
			t.start()

		for t in threads:
			t.join()

		return self.responsive_address

	def scanInterfaces(self):
		interfaces = get_windows_if_list()
		interface_names = [interface['name'] for interface in interfaces]
		interfaces_with_traffic = []
		print(" Scanning Interfaces:")

		with tqdm(total=len(interface_names), bar_format=' {l_bar}{bar}|', ncols=50) as pbar:
			for interface in interface_names:
				try:
					packets = sniff(filter="", count=10, iface=interface, timeout=3)
					if packets:
						interfaces_with_traffic.append(interface)
				except:
					pass

				pbar.update(1)

		return interfaces_with_traffic