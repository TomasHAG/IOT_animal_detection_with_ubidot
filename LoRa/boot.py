
from network import LoRa
import socket
import time
import struct
import keys
import light_manager

# Initialise LoRa in LORAWAN mode. Using EU region
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(keys.eui(), keys.key()), timeout=0)

while not lora.has_joined(): # chack if connected
    light_manager.look_foor_connection() # show with light that it still looking
    print('Not yet joined...')
    time.sleep(3)

print("Joined network")
light_manager.connected() # show with lights that it find network

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

#define which port with the socket bind
s.bind(2)# init port

s.setblocking(False)
# get any data received...
