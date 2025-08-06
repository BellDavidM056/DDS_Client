import zmq
import threading
import time
import json

class DDSClient:
    def __init__(self, pub_port=None, sub_port=None, name="DDSClient"):
        self.context = zmq.Context()
        self.name = name
        # Publisher setup
        if pub_port:
            self.pub_socket = self.context.socket(zmq.PUB)
            self.pub_socket.bind(f"tcp://*:{pub_port}")
        else:
            self.pub_socket = None

        # Subscriber setup
        if sub_port:
            self.sub_socket = self.context.socket(zmq.SUB)
            self.sub_socket.connect(f"tcp://localhost:{sub_port}")
            self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        else:
            self.sub_socket = None

    def publish(self, message):
        if self.pub_socket:
            time.sleep(0.1)  # Allow subscribers to connect
            print(f"[{self.name}] Publishing: {message}")
            self.pub_socket.send_json(message)

    def listen(self, callback):
        def _listen():
            while True:
                try:
                    msg = self.sub_socket.recv_json()
                    print(f"[{self.name}] Received: {msg}")
                    callback(msg)
                except Exception as e:
                    print(f"[{self.name}] Error: {e}")
                    break

        if self.sub_socket:
            thread = threading.Thread(target=_listen, daemon=True)
            thread.start()
