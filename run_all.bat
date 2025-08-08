@echo off
start cmd /k "python discovery_service.py"
start cmd /k "echo Press Enter to run client3.py & pause & python client3.py"
start cmd /k "echo Press Enter to run client2.py again & pause & python client2.py"
start cmd /k "echo Press Enter to run client1.py & pause & python client1.py"

