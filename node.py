#!/usr/bin/env python3
import asyncio
import random
from time import sleep
import json
from multiprocessing import Process, Pool
from threading import Thread
import subprocess
import time
import hashlib
import socket
import time

start_port = 6000

class Node(Process):

	# Time in ms
	MAX_NOMINATION_DURATION = 750 # Max Buffer Time before candidate declaration
	MIN_NOMINATION_DURATION = 250 # Min Buffer Time before candidate declaration
	ELECTION_DURATION = 500 # Wait Time to receive votes
	SESSION_TIMER = 10000 # Session duration before next election
	RESULT_CONFIRMATION_TIMER = 6000 # Wait Time to receive submissions from all followers
	CLUSTER_SIZE = 5 # Size of a cluster, set by default


	def run(self):
		thread1 = Thread(target = self.socket_listen)
		thread2 = Thread(target = self.election_handler)
		thread1.start()
		thread2.start()
		thread1.join()
		thread2.join()


	def __init__(self, node_id, default_nodes, default_local_leaders):
		self.id = node_id # Port No a node is running on
		self.history = [] # Set of all computations done
		self.CL = start_port # Central Leader of a node
		self.LL = None # Local Leader of a node
		self.task_queue = [] # Tasks a CL is running
		self.no_of_tasks_queued = 0 # No of tasks a CL has iin its queue that have not been processed
		self.local_leaders = default_local_leaders # List of all Local Leaders held by CL
		self.number_of_clusters = 0 # Total number of clusters
		self.all_node_info = default_nodes # Dict of all active ports to cluster no on the network
		self.ll_vote_count = -1 # Vote Count if this node is a local leader candidate
		self.cl_vote_count = -1  # Vote Count if this node is a central leader candidate
		self.has_ll_voted = False # True, if this node has voted during election
		self.has_cl_voted = False # True, if this node is LL and voted for a central leader
		self.is_election = False # True, if election is happening rn. Does not accept tasks if set to true

		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind((socket.gethostname(), self.id))
		self.serversocket.listen(20)  # upto 10 connections can be held in queue
		super(Node, self).__init__()

	# Create Task and send to CL
	def submit_to_leader(filename):
		code = """"""
		with open(filename + '.py', 'r') as f:
			code += f.read()
		data = {
			'code': code,
			'filename': filename
		}
		self.send_data_to_node('submission', data, self.CL)


	# Run a Task, done by followers
	def compute_data(submisison):
		codename = submisison['filename']
		code = submisison['code']
		filename = hashlib.sha1(str(time.time().encode())).hexdigest()
		with open(filename + '.py', 'w') as f:
			f.write(code)
		p = subprocess.Popen(['cat',  filename], stdout=subprocess.PIPE)
		output = ""
		out, err = p.communicate()
		inputs = out.decode().split('\n')
		for inp in inputs:
			if inp:
				proc = subprocess.Popen(['python', 'temp.py'], stdin=subprocess.PIPE)
				out, err = proc.communicate(input=l.encode())
				output += out + "\n"
		with open('temp_generated', 'w') as f:
			f.write(output)
		proc = subprocess.Popen(['diff', temp + '_generated', temp + '_answer'], stdout=subprocess.PIPE)
		out, err = proc.communicate()
		sending_data = {
			'question_id': codename,
			'status': out == ''
		}
		self.send_data_to_node('compute_result', sending_data, self.LL)


	# Open socket connection listening for other nodes
	# During Cluster Election,
	# 	Accept from same cluster only
	# During Central Election,
	# 	Accept from other LL only if LL
	# When not election,
	# 	Accept from CL and LL
	def socket_listen(self):
		while True:
			(clientsocket, address) = self.serversocket.accept()
			data = clientsocket.recv(1024)
			if not data:
				print("Sadly, something went wrong lol")

			data = json.loads(data.decode())

			if data['type'] == 'tx_history':
				self.receive_update_history(data['data'])
			if data['type'] == 'cluster':
				self.receive_cluster_info(data['data'])
			if data['type'] == 'll_vote_request':
				self.receive_ll_vote_request(data['data'])
			if data['type'] == 'll_vote':
				self.receive_ll_vote()
			if data['type'] == 'i_am_ll':
				self.receive_ll(data['data'])
			if data['type'] == 'local_leaders':
				self.receive_local_leaders(data['data'])
			if data['type'] == 'cl_vote_request':
				self.receive_cl_vote_request(data['data'])
			if data['type'] == 'cl_vote':
				self.receive_cl_vote()
			if data['type'] == 'i_am_cl':
				self.receive_cl(data['data'])


	def send_data_to_node(self, type_of_message, data, port):
		mySocket = socket.socket()
		sending_data = {
			'type': type_of_message,
			'data': data
		}
		sending_data = json.dumps(sending_data).encode()
		mySocket.connect((socket.gethostname(), int(port)))
		mySocket.sendall(sending_data)


	# Handles all election calls, runs on a thread
	def election_handler(self):
		while True:
			# Set Initial Values
			self.is_election = True
			self.has_ll_voted = False
			self.has_cl_voted = False
			sleep(0.5)
			
			print(self.id, " has started election process")
			# If CL, send tx history and cluster assignment details to all nodes
			# If not CL, wait for some time to let every node receive data
			
			start_sec = int(round(time.time() * 1000))
			if self.id == self.CL:
				print(self.id, " is the current CL, assigning clusters")
				self.assign_cluster()
				print("Current cluster assignment is ", self.all_node_info)
				for key in self.all_node_info.keys():
					self.send_data_to_node('tx_history', self.history, key)
					self.send_data_to_node('cluster', self.all_node_info, key)
				end_sec = int(round(time.time() * 1000))
				if((end_sec - start_sec) < 1000):
					sleep((1000 - (end_sec - start_sec)) / 1000)
			else:
				sleep(1)

			print(self.id, " has synchronized data with central node")
			print(self.id, " participating in cluster election...")
			
			start_sec = int(round(time.time() * 1000))
			# Cluster Election
			self.cluster_election()
			end_sec = int(round(time.time() * 1000))
			if((end_sec - start_sec) < 1000):
				sleep((1000 - (end_sec - start_sec)) / 1000)

			print("Local Leader voting done for ", self.id)

			# If Cluster Leader, send new local leaders to every other one
			start_sec = int(round(time.time() * 1000))
			if self.id == self.CL:
				for key in self.all_node_info.keys():
					self.send_data_to_node('local_leaders', self.local_leaders, key)
				end_sec = int(round(time.time() * 1000))
				if((end_sec - start_sec) < 500):
					sleep((500 - (end_sec - start_sec)) / 1000)
			else:
				sleep(0.5)

			print("Local Leader of ", self.id, " - ", self.local_leaders[str(self.all_node_info[str(self.id)])])

			self.CL = -1
			# Clear existing CL, do network selection
			start_sec = int(round(time.time() * 1000))
			if self.local_leaders[str(self.all_node_info[str(self.id)])] == self.id:
				print("Local Leader ", self.id, " initiates network selection")
				self.network_election()
				end_sec = int(round(time.time() * 1000))
				if((end_sec - start_sec) < 1000):
					sleep((1000 - (end_sec - start_sec)) / 1000)
			else:
				sleep(1)

			print("Central Leader of ", self.id, " is ", self.CL)
			# Wait for session to end
			self.is_election = False

			print("Starting next session at ", self.id, "...")
			sleep(Node.SESSION_TIMER / 1000)


	# Assign Cluster Ids for every node, only used by CL
	def assign_cluster(self):
		num_nodes = len(self.all_node_info)
		num_clusters = num_nodes // Node.CLUSTER_SIZE
		
		random_assign = []
		for x in range(0, num_clusters):
			for y in range(0, Node.CLUSTER_SIZE):
				random_assign.append(x)
		random.shuffle(random_assign)
		
		index = 0
		for key in self.all_node_info:
			self.all_node_info[str(key)] = random_assign[index]
			index += 1


	# Cluster election happens
	# Wait for randomized nomination time, Send vote request to every one in cluster
	# Wait for responses, if majority, send to every cluster node saying I am LL
	# Send information to CL
	def cluster_election(self):
		if self.has_ll_voted:
			return
		
		# Wait for Nomination Buffer Time
		nomination_wait_time = random.randint(Node.MIN_NOMINATION_DURATION, Node.MAX_NOMINATION_DURATION)
		sleep(nomination_wait_time / 1000)

		if self.has_ll_voted:
			return

		# Send vote requests
		cluster_no = self.all_node_info[str(self.id)]
		self.ll_vote_count = 1
		self.has_ll_voted = True
		for key in self.all_node_info:
			if self.all_node_info[str(key)] == cluster_no:  # same cluster
				self.send_data_to_node('ll_vote_request', self.id, key)
		
		# Wait for everyone to send votes
		sleep(Node.ELECTION_DURATION / 1000)

		# If majority, Send to all nodes in network
		if self.ll_vote_count > (Node.CLUSTER_SIZE // 2):
			self.send_data_to_node('i_am_ll', self.id, self.CL)
		else:
			sleep(2)


	# Central Leader Election
	# Randomly select one central leader out of existing LLs
	# Transfer cluster data to every node
	def network_election(self):
		if(self.local_leaders[str(self.all_node_info[str(self.id)])] == self.id):
			if self.has_cl_voted:
				return
			
			nomination_wait_time = random.randint(Node.MIN_NOMINATION_DURATION, Node.MAX_NOMINATION_DURATION)
			sleep(nomination_wait_time / 1000)

			# Send vote requests
			if self.has_cl_voted:
				return


			self.cl_vote_count = 1
			self.has_cl_voted = True
			for key in self.all_node_info:
				if(int(key) == self.local_leaders[str(self.all_node_info[str(key)])]):
					self.send_data_to_node('cl_vote_request', self.id, key)
			
			sleep(Node.ELECTION_DURATION / 1000)

			if self.cl_vote_count > 1:
				for key in self.all_node_info:
					self.send_data_to_node('i_am_cl', self.id, key)

	# Pre Election Broadcast from CL about current history
	def receive_update_history(self, tx_history):
		self.history.append(tx_history)


	# Update all node info
	def receive_cluster_info(self, all_node_info):
		self.all_node_info = all_node_info


	# Received a vote request from another node from same cluster, vote for it if not already voted
	def receive_ll_vote_request(self, id):
		if not self.has_ll_voted and self.all_node_info[str(id)] == self.all_node_info[str(self.id)]:
			self.has_ll_voted = True
			self.send_data_to_node('ll_vote', 'NIL', id)


	# Receieved vote for this node, check if valid and update
	def receive_ll_vote(self):
		if self.ll_vote_count != -1:
			self.ll_vote_count += 1


	# Received information saying that ll_id is the Local Leader now
	def receive_ll(self, ll_id):
		self.local_leaders[str(self.all_node_info[str(ll_id)])] = ll_id


	# Received list of all local leaders
	def receive_local_leaders(self, local_leaders):
		self.local_leaders = local_leaders


	# Received a vote request from another local leader, vote for it if not already voted
	def receive_cl_vote_request(self, id):
		if self.has_cl_voted == False and id == self.local_leaders[str(self.all_node_info[str(id)])]:
			self.has_cl_voted = True
			self.send_data_to_node('cl_vote', '', str(id))


	# Receieved vote for this node, check if valid and update
	def receive_cl_vote(self):
		if self.cl_vote_count != -1:
			self.cl_vote_count += 1


	# Received information saying that cl_id is the Central Leader now
	def receive_cl(self, cl_id):
		if self.id == self.local_leaders[str(self.all_node_info[str(self.id)])]:
			self.has_cl_voted = True
		self.CL = cl_id

if __name__ == '__main__':
	n = 15  # number of processses to run in parallel
	default_nodes = {}
	default_local_leaders = {'0': start_port, '1': start_port+5, '2': start_port+10}
	for i in range(n):
		default_nodes[str(start_port+i)] = i//5
	proc = []
	for i in range(n):
		p = Node(start_port + i, default_nodes, default_local_leaders)  # port numbers go from 5000 to 5000 + n - 1
		proc.append(p)
		p.start()
	for p in proc:
		p.join()
