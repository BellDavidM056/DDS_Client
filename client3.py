import zmq
import time
from dds_client import DDSClient

def relay_to_client1(msg):
    final_msg = {
        "id": 3, #msg["id"],
        "text": f"Relayed: {msg['text']}",
        "source": "Client3"
    }
    client3.publish(final_msg)

# Connect to discovery service
context = zmq.Context()
disc_socket = context.socket(zmq.REQ)
disc_socket.connect("tcp://localhost:6000")

# Register Client3
disc_socket.send_json({
    "register": "Client3",
    "pub_port": 5557,
    "sub_port": 5556
})
disc_socket.recv_json()

# Retry until Client2 is registered
client2_info = {}
while "pub_port" not in client2_info:
    disc_socket.send_json({"query": "Client2"})
    client2_info = disc_socket.recv_json()
    if "pub_port" not in client2_info:
        print("[Client3] Waiting for Client2 to register...")
        time.sleep(1)

client3 = DDSClient(pub_port=5557, sub_port=client2_info["pub_port"], name="Client3")
client3.listen(relay_to_client1)

while True:
    time.sleep(1)
