import json
import os
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Method", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("".encode("utf-8"))

    def do_POST(self):
        if self.path == "/register":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            id = payload["id"]
            password = payload["password"]

            if os.path.exists("users.json"):
                with open("users.json", "r") as file:
                    users = json.load(file)
            else:
                users = {}

            if id in users:
                self.send_response(400)
                self.end_headers()
                response = {"success": False, "message": "ID already registered"}
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )
            else:
                users[id] = password

                with open("users.json", "w", encoding="utf-8") as file:
                    json.dump(users, file)

                self.send_response(200)
                self.end_headers()
                response = {"success": True, "id": id}
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )

        if self.path == "/login":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            payload = json.loads(body)

            id = payload["id"]
            password = payload["password"]

            if os.path.exists("users.json"):
                with open("users.json", "r") as file:
                    users = json.load(file)
            else:
                users = {}

            if id not in users or users[id] != password:
                self.send_response(400)
                self.end_headers()
                response = {"success": False, "message": "ID or password is incorrect"}
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )
            else:
                session_id = "session"

                cookie = SimpleCookie()
                cookie["session"] = session_id
                self.send_header("Set-Cookie", cookie.output(header=""))

                self.send_response(200)
                self.end_headers()
                response = {"success": True, "id": id, "sessionId": session_id}
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )

server_address = ("0.0.0.0", 8080)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.serve_forever()
