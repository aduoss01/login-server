from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Method', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')        
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):    
        self.send_response(200)
        self.end_headers()
        self.wfile.write("".encode("utf-8"))
        
    def do_POST(self):
        """
        Method: POST
        Path: /register
        Body: {"id": "", "password": ""}
        Result: {"success": true, "id": ""}
        """
        if self.path == '/register':            
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            id = payload['id']
            password = payload['password']


        """ 
        Method: POST
        Path: /login
        Body: {"id": "", "password": ""}
        Result: {"success": true, "id": "", "sessionId": ""}
        Cookie: session=...
        """
        if self.path == '/login':
            pass
        
server_address = ('0.0.0.0', 8080)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.serve_forever()