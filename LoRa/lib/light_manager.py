import pycom
import time
import _thread
pycom.heartbeat(False) # deactivate hearthbeat
lock = _thread.allocate_lock() # Initialise thread lock

def light(delay, color, times): # logistics for light controlls
    with lock:
        for i in range(times): # multiple blinkings
            pycom.rgbled(color) # turn on with specifik color
            time.sleep(delay) # #delay
            pycom.rgbled(0x000000) # turn of light
            if times > 1:
                time.sleep(delay) # dalay between blinkings


def look_foor_connection(): # 1 secound light yellow light once
    _thread.start_new_thread(light, (1, 0xff7700, 1))

def connected(): # green blinking 3 times with 0.2 secounds on eatch
    _thread.start_new_thread(light, (0.2, 0x00ff00, 3))

def data_send(): # white blinking 4 times with 0.1 secounds on eatch
    _thread.start_new_thread(light, (0.1, 0xffffff, 4))

def data_reserved(): # 1 secound light blue light once
    _thread.start_new_thread(light, (1.5, 0x0000ff, 1))
