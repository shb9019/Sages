
# SAGES
A decentralized Competitive Coding platform which allows users to host contests, join contests, write code and submit codes with no central point of authority or failure.

*Under Ideation and Development*

## Table of contents

 - Introduction
 - Why decentralize?
 - Working Principle
 - Organizing a contest
 - Elections
 - Submissions & Evaluation
 - Why this architecture?
 - Issues
 - Progress
 - Contributors

## Introduction

A decentralized application which allows you to participate and organize coding contests. This application provides an IDE to submit, view results, see problem statements etc like any normal competitive coding platform would (Something that looks like Topcoder interface) while completely abstracting away the internal workings. Every *node* participating in a contest including the organizers (hereafter referred to as *sages*) form a part of the contest *community*. The responsibility of distributing the problem statements and evaluating submissions lies completely on the network. Every node gives the community its computational power proportional to the amount it is using.

## Why Decentralize?

The reasons are same as for why we need any decentralized application (Dapp).

 - Improve fault tolerance and make it expensive and practically impossible to attack.
 - Remove the concept of a centralized authority overwatching the contest and have the right to tamper with or use the data.
- Not being a victim for the errors and mistakes of another authority.

In the specific case of competitive coding, there have been innumerable cases where a contest is spoiled due to server issues of the platform. There is no concept of privacy when its centralized. Though privacy is not of primary concern in competitive coding, **the scope of this project model is not limited to evaluating code submissions**.

## Working Principle
The whole community is divided into *clusters* and each cluster has a *cluster head*. There is a *central leader* which is one of the cluster heads.

The complete duration of a contest is split into *sessions* and at the beginning of every session, *elections* happen where the cluster leader for every cluster and the central leader from the cluster leaders are elected.

The previous session central leader disseminates information about the current network, the status of leaderboard and list of submissions to the new cluster leaders after the cluster leader elections. The central leader then initiates the new session's central election and steps down to a normal node.

When a node wants to submit code to a specific problem, it submits to the current central leader. The central leader then sends the submission to the cluster with the lowest workload while keeping track of which cluster the submission has been done to.

The cluster leader will in turn submit the problem to all *subordinates* in its cluster. The subordinates evaluate and submit the result of the problem. The maximum of the evaluation result (Assuming to be boolean, Wrong or Right) is taken as the final result and submitted back to the central leader.

The central leader stores the submission result and passes on the data to the node which requested the evaluation (Note: The node which has requested the evaluation can also be the one evaluating).

## Organizing a contest

Every contest starts with a set of *sage* nodes which belongs to the contest organizers. Any node which wants to register for the contest sends a registration request to one of the sage nodes which then sends the confirmation or rejection reply along with the contest details and current community information. The sage nodes communicate with each other keeping track of all the registrations for the contest.

An online forum can exist to post the set of contests along with the corresponding sage IP Addresses. When a participant wants to register, he enters the set of valid sage addresses.

The greater the number of sage nodes, the lower the workload on each sage node. It is also helpful to have the sage nodes evenly distributed throughout the internet to reduce access latencies.

At least one of the sage nodes have to be online during the registration period, which can range from 10 mins to 5 hours, to keep the contest alive. In case all the sage nodes go offline, the last sage node which goes offline can transfer its sage authority to another registered node.

Anyone can organize a contest by choosing to be a sage and preloading the corresponding data such as problem statements, encrypted test cases, partner sages and other contest details.

Before the start of a contest, the contest information are broadcasted to all registered nodes.

## Elections

### Cluster Elections

Assuming there is a cluster structure currently defined (i.e., the information of which node belongs to which cluster) and every node is aware of its own cluster, at the beginning of every session, cluster elections happens where every node in a cluster votes for the corresponding cluster's leader.

At the beginning of a cluster election, ever node waits for a randomized amount of time before multicasting out a vote request to all nodes in the cluster asking for that node to for the *candidate* which is the sender of the vote request. Once a node chooses to be a candidate, it cannot vote for any other node and the first vote is by itself.

On receiving a vote request, if the node hasn't voted for any other candidate, it votes for the first vote request it receives by sending a vote message to the candidate. On receiving a vote message, a candidate increments the number of votes it has. After voting for a node or sending vote request, the node starts an election timer, which is the max amount of time the election can last for.

At the end of election period (a fixed duration), the candidate which has number of votes which is atleast half the number of nodes in the request, it sends a multicast message to all members of the cluster announcing itself as the new cluster leader and sends back a message to the existing central leader regarding the same.

On receiving a leader announcement, the election timer is killed and a new session timer is started. In case no node receives majority which is known by the election timer timing out, a re-election happens. The number of re-elections depends on the distribution of the randomization algorithm choosen and also the network latencies between nodes of the cluster.

On receiving the cluster leader announcement by the previous session's cluster leader, the list of pending task evaluations are sent to the new cluster leader by it. In case there is any task which is being executed by the current central leader before the start of the session, it finishes the execution of that task.

### Central Elections

The central elections are very similar in principle to the cluster elections. On the start of a session, the cluster elections happen. Every newly elected cluster leader sends back the results of the corresponding cluster election and announces itself as the cluster's leader. Once the current central leader has received cluster election results from every cluster in the community, it initiates a central leader election by sending out a multicast message to all central leaders in the community informing that the election has started.

As in the case of cluster elections, vote requests are sent and vote replies are sent back. Upon receving majority, a node becomes the central leader and broadcasts this announcement to all nodes in the whole community. The previous central leader sends all information such as network status, cluster information, submissions status, leaderboard, pending submissions in the queue etc. All other nodes in the network must wait for a specific interval to wait for this handoff to complete.

The central leader also has the responsibility of creating the new cluster configuration for the next session. If the geographic distribution of nodes is large, it is better to assign clusters based on the region to reduce the communication latency.

## Submissions and Evaluation

When a node in the community wants to submit a solution to a specific problem, the code is wrapped as a task along with other information such as the sending node, problem id, input test cases, submission time etc and is sent to the central leader.

The central node upon receiving a submission stores the submission data most importantly the sending node address. The cluster with the lowest workload i.e., the smallest number of pending submissions, is chosen and the task is sent storing the cluster id correspondingly. An evaluation timer is set once the task is sent to a cluster leader on expiration of which another cluster is chosen to evaluate.

The cluster leader upon receiving a task, sends this to all its subordinates in the cluster for evaluation. The node which receives a task to evaluate, compiles, executes and sends back the result to the cluster leader. The cluster leader keeps track of the results from each subordinate and in case there is no result which is sent by the majority of the subordinates a failure message is sent back to the central leader, which sends this task to another cluster.

During elections, tasks are submitted to the previous session's central leader. To the submitting nodes, the process is the exact same as it was in the previous session. Until the new leader is elected, the previous leader should do its job.

## Why this architecture?

### Concept of clusters
The submissions made by every node must be executed by at least one node. If we assume that a submission from one node is evaluated by exactly one other node, there is a possibility of mailicious node which gives wrong answers to all submissions. To avoid this, there is only one solution to this which is instead of trusting a single node, we redundantly send this task to multiple nodes and selecting the majority answer. Though this does increase the amount of computation done, it ensures that the submissions are evaluated correctly. The number of nodes in a cluster can be parameterized to acheive a balance between the load and the accuracy.

### Elections
Having a single leader throughout the contest duration is not ideal since there is a possibility of the node acting malicious and manipulating the submission results being sent.

### Sages
Before the start of a contest, it is usually not expected of a node to be online so there is a necessity of having a couple of nodes which are guaranteed to be online and can be a authorized point of communication. Also, to get connected to a community, it is necessary to connect to at least one node in the community. Being decentralized, it is natural to have a set of seed peers to connect to and slowly discover other peers in the network.

## Issues

### 1. What happens when a subordinate node goes offline?
Every cluster leader sends a heartbeat message regularly to every node in the cluster. In case the cluster leader does not receive a heartbeat echo message from the node, the node is assumed to be dead. If a node comes back live, it sends back a heartbeat echo with no solicitation to the corresponding cluster leader.

In case the node comes live in another session, the heartbeat echo is sent to the cluster leader that existed when it was live, if the node the echo message is sent to is not the current cluster leader, a reply is sent back with the current cluster leader.

If there is no response for the heartbeat echo sent, a request to one of the sages is sent asking for the central leader address and further asks the central leader for it's cluster leader.

### 2. What happens when a cluster leader goes offline?
Every node in a cluster have a heartbeat timer which is the time before which it must receive a heartbeat from the cluster leader. If not received, a new election starts by sending out vote requests. The central leader also tracks the liveliness of the cluster leaders using corresponding heartbeats. Upon receiving any message from a cluster leader, the heartbeat timer is reset.

### 3. What happens when the central leader goes offline?
Similar to the case when a cluster leader fails, a new election is started.

### 4. What happens when a subordinate node behaves malicious?
Due to redundancy of task evaluated, even if a node does act malicious and submits wrong results there are other nodes which act rightfully. Since the chances of having wrong result by maliciously acting subordinate nodes is only when majority of nodes in a cluster are malicious. And the probability of a node being in a cluster is 1/(the number of clusters). It is possible to control the contest and giving out wrong submissions is only when at least 51% of the community consists of the attacker's nodes.

### 5. What happens when a cluster leader behaves malicious?
I haven't given this much thought yet, but one of the solutions is to send a verification problem as a task to check if the cluster leader isn't acting malicious.

### 6. What happens when the central leader behaves malicious?
Open to suggestions :)

### 7. What happens if any node is behind a NAT?
Assuming every node has a unique public address, this shouldn't be an issue.

### 8. What happens if a node sends a authoritarian message such as tasks etc acting to be a cluster leader or central leader?
The messages are signed by the sending node using it's private key which can only be verified by it's own public key. This way we can ensure that a node is actually from the corresponding sender.

### 9. What happens if all nodes of the community goes offline?
There is nothing that can be done, we have lost the data :)

### 10. What happens if a node sends out leader announcement messages without actually being elected as the leader?
The newly elected cluster leader must also send the corresponding list of nodes which voted for it. In case a node finds out that it hasn't voted for the cluster leader but it's address has been included or there are less than 51% of nodes voting for that cluster leader, it can start a new election round immediately.

## Progress

 - [ ] Ideation
 - [ ] Peer Network System
 - [ ] Elections
 - [ ] Contest Registrations
 - [ ] Problem Submissions
 - [ ] Handling Node Failures
 - [ ] Security Issues

## Contributors

 - [Akshay Pai](https://github.com/PaiAkshay998)
 - [Sai Hemanth B](https://github.com/shb9019)