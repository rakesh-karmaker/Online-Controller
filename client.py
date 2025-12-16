import socket
import os
from dotenv import load_dotenv
import vgamepad as vg
from inputs import get_gamepad

# Load variables from .env into environment
load_dotenv()

SERVER_IP_ADDRESS = os.getenv('SERVER_IP_ADDRESS', '')
SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))

# Create a UDP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# initialize the virtual gamepad
gamepad = vg.VX360Gamepad()

while True:
    events = get_gamepad()
    for event in events:
        controller_input = f"{event.ev_type},{event.code},{event.state}"
        clientSocket.sendto(controller_input.encode(), (SERVER_IP_ADDRESS, SERVER_PORT))
