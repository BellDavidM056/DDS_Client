import zmq
import time
from dds_client import DDSClient

def relay_to_client3(msg):
    relayed_msg = {
        "id": 2, #msg["id"],
        "text": f"Relayed: {msg['text']}",
        "source": "Client2"
    }
    client2.publish(relayed_msg)

# Connect to discovery service
context = zmq.Context()
disc_socket = context.socket(zmq.REQ)
disc_socket.connect("tcp://localhost:6000")

# Register Client2
disc_socket.send_json({
    "register": "Client2",
    "pub_port": 5556,
    "sub_port": 5555
})
disc_socket.recv_json()

# Retry until Client1 is registered
client1_info = {}
while "pub_port" not in client1_info:
    disc_socket.send_json({"query": "Client1"})
    client1_info = disc_socket.recv_json()
    if "pub_port" not in client1_info:
        print("[Client2] Waiting for Client1 to register...")
        time.sleep(1)

client2 = DDSClient(pub_port=5556, sub_port=client1_info["pub_port"], name="Client2")
client2.listen(relay_to_client3)

while True:
    time.sleep(1)
