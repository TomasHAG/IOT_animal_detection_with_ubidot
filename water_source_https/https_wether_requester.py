from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from pyowm import OWM
import json
import base64
import codecs

import mysql_handler as mh


password = 'password123' #password for more secure connection

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global password #import password
        print("GET triggered")

        if not self.headers['Authorization'] == password: # security check
            print("Wrong password")
            return

        #load info from content headern
        req = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
        req = json.loads(req)
        print(req)

        location = 'Sjöbo,SE' #location of weather station
        owm = OWM('e2bc44778d5f1c9c0cdc7177e10c2e8e')   #api key for open weather api

        #init and get an wether observation
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        w = observation.weather

        #calculate hex value for wind and temprature
        T = hex( int(( w.temperature('celsius')['temp'] + 10 ) * (255/50)) )[2:].zfill(2)
        W = hex(  int( w.wind()['speed'] * (255/40) ) )[2:].zfill(2)

        #calculate byte value for humidity and clud dencity
        H = hex(  int( w.humidity * (15/100) ) )[2:].zfill(1)
        C = hex(  int( w.clouds * (15/100) ) )[2:].zfill(1)

        print("hex to send: " + T + W + H + C) #show hex to send in console

        #encode the payload to send to base 64
        payload =  codecs.encode(codecs.decode(T + W + H + C, 'hex'), 'base64').decode()

        #skip send an wether update for the device if there are no changes
        if req['payload_raw'] == payload[:-1]:
            print("no response")
            return

        #create content header to send
        out_data = {
            'dev_id': req['dev_id'],    # The device ID
            'port': 1,                  # LoRaWAN FPort
            'confirmed': False,         # Whether the downlink should be confirmed by the device
            'payload_raw': payload      # payload: [0x01, 0x02, 0x03, 0x04]
        }

        #send data
        r = requests.post(req['downlink_url'], json=out_data)
        print(r)#print response code. 202 is success and 400 is failure

    def do_POST(self):
        global password #import password
        print("GET triggered")

        if not self.headers['Authorization'] == password: # security check
            print("Wrong password")
            return

        #load info from content headern
        req = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
        req = json.loads(req)
        print(req)
        payload = req["payload_fields"]
        time = req["metadata"]["time"]
        time = time.replace("T", " ")
        time = time.replace("Z", "")
        mh.input_data(req["dev_id"], time, payload["temperature"],
                    payload["wind"], payload["humidity"], payload["clouds"],
                    payload["sensor_trigger"])

def main():
    PORT = 9123 #define port
    server_address = ('', PORT) #address is this computers ip adress
    server = HTTPServer(server_address, requestHandler) #start server
    print(f'server running on port {PORT}')
    server.serve_forever()#run it until closed

if __name__ == '__main__':
    main()
