import detector
import time
import light_manager

weather_data = b'0x01010101'

def lora_cb(lora): # initilize logic for callback to get and send packages.
    global weather_data # global to get accsess to wether data in callbacks
    events = lora.events()
    #when a package is detected inbound update wether to inbound wether
    if events & LoRa.RX_PACKET_EVENT:
        light_manager.data_reserved()
        weather_data = s.recv(64)

    if events & LoRa.TX_PACKET_EVENT: # send package with wether data
        light_manager.data_send()

# activate callbacks
lora.callback(trigger=(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT), handler=lora_cb)

def send(port): # send wether data from memory to a specifik port
    s.bind(port) # bind to the new port
    s.send(weather_data) # send wether data

def loop(): # internal loop to detect and send data
    counter = 0
    send(4) # init send, to get first wether data
    while True:
        time.sleep(2) # loop in 2 sec intervalls
        counter += 1
        if detector.read():
            send(2) # send in port 2 that an animal have ben detected
            time.sleep(1*60) # after detection trigger sleep for 1 minute
            counter = 0 # reset echo counter
        elif counter > 10*30: # every 10 minutes
            send(3) #port 3 is for echo calls
            counter = 0 # reset echo counter

loop()
