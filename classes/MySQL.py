import mysql.connector
import random
import sys

class MySqlCommands():
	def __init__(self):
		self.host = "localhost"
		self.user = "root"
		self.password = ""
		self.database = "NetGuard"
		self.cursor = None
		self.connection = None

	def connectDB(self):
		try:
			self.connection = mysql.connector.connect(
				host=self.host,
				user=self.user,
				password=self.password,
				connect_timeout=30
			)

			self.cursor = self.connection.cursor()
			self.cursor.execute("SHOW DATABASES LIKE '{}'".format(self.database))
			db_exists = self.cursor.fetchall()

			if db_exists:
				self.cursor.execute("USE {}".format(self.database))
				return

			self.cursor.execute("CREATE DATABASE {}".format(self.database))
			self.cursor.execute("USE {}".format(self.database))

			self.cursor.execute("""
				CREATE TABLE users(
					ID INT AUTO_INCREMENT PRIMARY KEY,
					UniqueID INT(9) ZEROFILL,
					Fname VARCHAR(100),
					Lname VARCHAR(100),
					Description VARCHAR(150),
					IP_address VARCHAR(45),
					Mac_address VARCHAR(17),
					Blocked_websites TEXT
				)
			""")

		except mysql.connector.Error as e:
			if isinstance(e, mysql.connector.errors.InterfaceError):
				print("\nError: Connection to MySQL refused. Please check the status or the MySQL server configuration.")
			else:
				print("\nAn error occurred: ", str(e))
    
			sys.exit(1)

	def closeConnection(self):
		try:
			self.cursor.close()
			self.connection.close()
		except Exception as e:
			print(f" Closing connection failed: {str(e)}\n")

	def generateUniqueID(self):
		try:
			while True:
				unique_ID = random.randint(100000000, 999999999)
				self.cursor.execute("SELECT * FROM users WHERE UniqueID = %s ", (unique_ID,))
				result = self.cursor.fetchone()
				if result is None:
					break
			return unique_ID
		except Exception as e:
			print(f" Generating unique ID failed: {str(e)}\n")
			sys.exit(1)

	def insertUser(self, Fname=None, Lname=None, Description=None, IP_address=None, Mac_address=None, Blocked_websites=None):
		self.connectDB()

		unique_ID = self.generateUniqueID()
		query = "INSERT INTO users VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)"
		values = (unique_ID, Fname, Lname, Description, IP_address, Mac_address, Blocked_websites)

		try:
			self.cursor.execute(query, values)
			self.connection.commit()
			print(" Insertion successful.\n")

		except Exception as e:
			self.connection.rollback()
			print(f" Insertion failed: {str(e)}\n")

		self.closeConnection()

	def updateUser(self, column, new_value, ID):
		self.connectDB()

		query = "UPDATE users SET {} = %s WHERE ID = %s".format(column)

		try:
			self.cursor.execute(query, (new_value, ID))
			self.connection.commit()
			print(" Update successful.\n")

		except Exception as e:
			self.connection.rollback()
			print(f" Update failed: {str(e)}\n")

		self.closeConnection()

	def deleteUser(self, ID):
		self.connectDB()

		query = "DELETE FROM users WHERE ID = %s"
		
		try:
			self.cursor.execute(query, (ID,))
			self.connection.commit()
			print(" User successfully deleted.\n")
		except Exception as e:
			self.connection.rollback()
			print(f" Deleting failed: {str(e)}\n")

		self.closeConnection()

####################################################################################
####################################################################################

	def getAllInfo(self):
		self.connectDB()

		try:
			self.cursor.execute("SELECT * FROM users")
			result = self.cursor.fetchall()
		except Exception as e:
			print(f" Query failed: {str(e)}\n")

		self.closeConnection()
		return result
	
	def getAllMacAddress(self):
		self.connectDB()

		try:
			self.cursor.execute("SELECT Mac_address FROM users")
			query = self.cursor.fetchall()
			result = [item[0] for item in query]
		except Exception as e:
			print(f" Query failed: {str(e)}\n")

		self.closeConnection()
		return result

	def getNames(self, MAC):
		self.connectDB()
		values = []

		if MAC:
			for address in MAC:
				try:
					self.cursor.execute("SELECT Fname, Lname, Description, IP_address, Mac_address FROM users WHERE Mac_address = %s", (address,))
					result = self.cursor.fetchall()
					if not result:
						return print(f" No info found with that Mac-address: {address}\n")
					values.append(result[0])
				except Exception as e:
					print(f" Query Failed: {str(e)}\n")

		self.closeConnection()
		return values
	




"""
FIXME: 
For each network this script is run on:
	- create a database with the name of the network: "NetGuard_LunaTelekom", "NetGuard_Home", etc.
	or
	- create a table with the name of the network: "LunaTelekom", "Home", etc.
	or
	- create a new table "network_names" and store the names of the networks there with a primary key. and add a new column for the table "users" and connect the primary key from "network_names" to each user. (to know which user is connected to which network) 

"""