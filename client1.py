from dds_client import DDSClient
import time

client1 = DDSClient(pub_port=5555,sub_port=5557, name="Client1")

# Give subscribers time to connect
time.sleep(1)

client1.publish({"id": 1, "text": "Hello from Client 1", "source": "Client1"})

time.sleep(1)

client1.listen(lambda msg: print(f"[Client1] Final message: {msg}"))

while True:
    time.sleep(1)