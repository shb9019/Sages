
# DVerify
A decentralized Competitive Coding platform which allows users to host contests, join contests, write code and submit codes with no central point of authority or failure.

*Under Ideation and Development*

## Table of contents

 - Introduction
 - Why decentralize?
 - Working Principle
 - Organizing a contest
 - Elections
 - Submissions & Evaluation
 - Validity
 - Issues

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