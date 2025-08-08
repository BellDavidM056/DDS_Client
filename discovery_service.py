import zmq
import json

registry = {}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:6000")  # Discovery service port

print("[Discovery] Service started...")

while True:
    message = socket.recv_json()
    response = {}

    if "register" in message:
        name = message["register"]
        registry[name] = {
            "pub_port": message["pub_port"],
            "sub_port": message["sub_port"]
        }
        print(f"[Discovery] Registered {name}")
        response = {"status": "registered"}

    elif "query" in message:
        target = message["query"]
        response = registry.get(target, {"error": "not found"})

    socket.send_json(response)
