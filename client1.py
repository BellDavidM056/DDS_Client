import zmq
import time
from dds_client import DDSClient

# Setup discovery connection
context = zmq.Context()
disc_socket = context.socket(zmq.REQ)
disc_socket.connect("tcp://localhost:6000")

# Register with discovery
disc_socket.send_json({
    "register": "Client1",
    "pub_port": 5555,
    "sub_port": 5557
})
disc_socket.recv_json()

# Query for Client2's pub port
disc_socket.send_json({"query": "Client2"})
client2_info = disc_socket.recv_json()

client1 = DDSClient(pub_port=5555, sub_port=client2_info["pub_port"], name="Client1")

time.sleep(1)
client1.publish({"id": 1, "text": "Hello from Client 1", "source": "Client1"})
time.sleep(1)
client1.listen(lambda msg: print(f"[Client1] Final message: {msg}"))

while True:
    time.sleep(1)
