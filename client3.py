import time
from dds_client import DDSClient


def relay_to_client1(msg):
    final_msg = {
        "id": msg["id"],
        "text": f"Relayed: {msg['text']}",
        "source": "Client3"
    }
    client3.publish(final_msg)

client3 = DDSClient(pub_port=5557, sub_port=5556, name="Client3")

client3.listen(relay_to_client1)


while True:
    time.sleep(1)
