#!/usr/bin/env python3
import asyncio

class Node:
    NOMINATION = 2
    END_OF_TERM = 10

    def __init__(self, node_id):
        self.id = node_id
        self.history = []
        self.CL = None
        self.LL = None
        self.task_queue = []
        self.no_of_tasks_queued = 0
        self.clusters = []
        self.number_of_clusters = []

    def submit_to_leader(task):
        pass

    def election_of_local_leader():
        pass

    def compute_data():
        pass    
