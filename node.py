#!/usr/bin/env python3
import asyncio
import random
from time import sleep

class Node:
	# Time in ms
	MIN_NOMINATION_DURATION = 750 # Min Buffer Time before candidate declaration
	MAX_NOMINATION_DURATION = 250 # Max Buffer Time before candidate declaration
	ELECTION_DURATION = 500 # Wait Time to receive votes
	SESSION_TIMER = 1800000 # Session duration before next election
	RESULT_CONFIRMATION_TIMER = 60000 # Wait Time to receive submissions from all followers
	CLUSTER_SIZE = 5 # Size of a cluster, set by default

	def __init__(self, node_id):
		self.id = node_id # Port No a node is running on
		self.history = [] # Set of all computations done
		self.CL = 5000 # Central Leader of a node
		self.LL = None # Local Leader of a node
		self.task_queue = [] # Tasks a CL is running
		self.no_of_tasks_queued = 0 # No of tasks a CL has iin its queue that have not been processed
		self.local_leaders = [] # List of all Local Leaders
		self.number_of_clusters = 0 # Total number of clusters
		self.all_node_info = [] # Dict of all active ports to cluster no on the network
		self.vote_count = -1 # Vote Count if this node is a candidate
		self.has_voted = False # True, if this node has voted during election
		self.is_election = False # True, if election is happening rn. Does not accept tasks if set to true
	
	# Create Task and send to CL
	def submit_to_leader(task):
		pass

	# Run a Task, done by followers
	def compute_data():
		pass
	
	# Pre Election Broadcast from CL about current history 
	def add_to_history(self, tx_history):
		self.history.append(tx_history)

	# Open socket connection listening for other nodes
	# During Cluster Election,
	# 	Accept from same cluster only
	# During Central Election,
	# 	Accept from other LL only if LL
	# When not election,
	# 	Accept from CL and LL
	def socket_listen():
		pass
	

	# Assign Cluster Ids for every node, only used by CL
	def assign_cluster(self):
		num_nodes = len(self.all_node_info)
		num_clusters = num_nodes / CLUSTER_SIZE
		
		random_assign = []
		for x in range(0,num_clusters):
			for y in range(0,CLUSTER_SIZE):
				random_assign.append(x)
		random.shuffle(random_assign)
		
		for key, idx in self.all_node_info:
			self.all_node_info[key] = random_assign[idx]

		for x in self.all_node_info:
			# Socket send new cluster info to all nodes


	# Cluster election happens
	# Wait for randomized nomination time, Send vote request to every one in cluster
	# Wait for responses, if majority, send to every cluster node saying I am LL
	# Send information to CL
	def cluster_election(self):
		# Wait for Nomination Buffer Time
		nomination_wait_time = random.randint(MIN_NOMINATION_DURATION, MAX_NOMINATION_DURATION)
		sleep(nomination_wait_time / 1000)

		# Send vote requests
		cluster_no = self.all_node_info[self.id]
		self.vote_count = 0
		for key,value in self.all_node_info.items():
			# Socket send vote request to nodes
		
		# Wait for everyone to send votes
		sleep(ELECTION_DURATION / 1000)

		if vote_count >= (CLUSTER_COUNT / 2):
			for key in self.all_node_info.items():
				if self.all_node_info[key] == cluster_no
					# Socket send I am local leader


	# Central Leader Election
	# Randomly select one central leader out of existing LLs
	# Transfer cluster data to every node
	def network_election():
		pass

	# Called by CL, once election is over
	def assign_to_LL():
		pass
	
	def assign_to_followers():
		pass

	def send_to_LL():
		pass
	
	def validate_answer():
		pass
	
	def send_to_CL():
		pass
