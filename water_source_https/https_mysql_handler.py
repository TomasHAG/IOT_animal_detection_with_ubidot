from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
import base64
import codecs

import mysql_handler as mh


password = 'password321' #password for more secure connection

class requestHandler(BaseHTTPRequestHandler):
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
    PORT = 9321 #define port
    server_address = ('', PORT) #address is this computers ip adress
    server = HTTPServer(server_address, requestHandler) #start server
    print(f'server running on port {PORT}')
    server.serve_forever()#run it until closed

if __name__ == '__main__':
    main()