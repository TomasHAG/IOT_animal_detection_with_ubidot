import machine

try: # error handling if file not existing
    f = open("pin_used.txt", "r") # open file
except:# if file not existing create one file with P18
    print("file is missing create default file")
    f = open("pin_used.txt", "w")
    f.write("P18")
    f.close()

    f = open("pin_used.txt", "r")

pin_used = f.read().split() # array of pin names to use
f.close() # close file 

adc = machine.ADC() # Initialise to use analog pin
pin = [] # list of pins
for p in pin_used: # create an analog pin for every pin name from file
    pin.append(adc.channel(pin=p))

adc = machine.ADC() # create an ADC object

def read(): # logistics to read all sensors
    for Pin in pin: # for every pin that are in use
        if Pin() > 0: # check if triggered
            return True # if any are triggered return true
    return False # if none is triggered return false

def redefine_pin_used(pin_names): # method to rewrite the file with what pin to use
    f = open("pin_used.txt", "w") # open with write
    f.write(pin_names) # write in new info
    f.close() # close file
    pin_used = pin_names.split() # reinitilize to be able to use the new pins
    pin = []
    for p in pin_used: # create an analog pin for every new pin name
        pin.append(adc.channel(pin=p))
