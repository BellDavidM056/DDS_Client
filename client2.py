import time
from dds_client import DDSClient


def relay_to_client3(msg):
    relayed_msg = {
        "id": msg["id"],
        "text": f"Relayed: {msg['text']}",
        "source": "Client2"
    }
    client2.publish(relayed_msg)


client2 = DDSClient(pub_port=5556, sub_port=5555, name="Client2")
client2.listen(relay_to_client3)

while True:
    time.sleep(1)
