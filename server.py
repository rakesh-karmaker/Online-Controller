import socket
import os
from dotenv import load_dotenv
import sys
import vgamepad as vg
from controller.gamepad import apply_payload_to_gamepad
from controller.state import current_axis_values
from inputs import get_gamepad

# Load variables from .env into environment
load_dotenv()

SERVER_IP_ADDRESS = os.getenv('SERVER_IP_ADDRESS', '')
SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))

# initialize the virtual gamepad
gamepad = vg.VX360Gamepad()

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_IP_ADDRESS, SERVER_PORT))

try:
    while True:
        # Receive controllerInput from client
        payload, client_address = server_socket.recvfrom(2048) # buffer size is 2048 bytes
        print(f"Received payload: {payload.decode()} from {client_address}")
        apply_payload_to_gamepad(gamepad, payload.decode(), current_axis_values)

        # send the server controllerInput to the user's virtual gamepad
        events = get_gamepad()
        for event in events:
            controller_input = f"{event.ev_type},{event.code},{event.state}"
            server_socket.sendto(controller_input.encode(), client_address)

except KeyboardInterrupt:
    print("Server is shutting down.")
    server_socket.close()
    sys.exit(0)