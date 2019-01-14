from network import Network
from time import sleep

n1 = Network(5000)
n2 = Network(5001)
n3 = Network(5002)
n4 = Network(5003)
n5 = Network(5004)

print("Nodes Created")
n1.sage_handler.create_contest()
print("Became Sage")
sleep(1)
n2.sage_handler.request_sage('ws://localhost:5000')
sleep(1)
n3.sage_handler.request_sage('ws://localhost:5000')
sleep(1)
n4.sage_handler.request_sage('ws://localhost:5000')
sleep(1)
n5.sage_handler.request_sage('ws://localhost:5000')