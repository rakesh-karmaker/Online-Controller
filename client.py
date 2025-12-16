import socket
import os
from dotenv import load_dotenv
import vgamepad as vg
from inputs import get_gamepad
from controller.gamepad import apply_payload_to_gamepad
from controller.state import current_axis_values

# Load variables from .env into environment
load_dotenv()

SERVER_IP_ADDRESS = os.getenv('SERVER_IP_ADDRESS', '')
SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# initialize the virtual gamepad
gamepad = vg.VX360Gamepad()

while True:
    # send the user's virtual gamepad input to the server
    events = get_gamepad()
    for event in events:
        controller_input = f"{event.ev_type},{event.code},{event.state}"
        client_socket.sendto(controller_input.encode(), (SERVER_IP_ADDRESS, SERVER_PORT))
    
    # Receive controllerInput from server
    payload, server_address = client_socket.recvfrom(4096) # buffer size is 4096 bytes
    print(f"Received payload: {payload.decode()} from {server_address}")
    apply_payload_to_gamepad(gamepad, payload.decode(), current_axis_values)
