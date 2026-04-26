import os
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from knowledge.graph_store import graph_store
from storage.db import db

STATIC_DIR = os.path.expanduser("~/hermuxclaw/dashboard/static")

class ProductionDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. API Endpoints
        if self.path == "/graph":
            self.send_json({
                "calls": graph_store.call_graph,
                "dependencies": graph_store.dep_graph
            })
        elif self.path == "/tasks":
            active = db.query("SELECT COUNT(*) FROM tasks WHERE status='processing'")[0][0]
            completed = db.query("SELECT COUNT(*) FROM tasks WHERE status='completed'")[0][0]
            pending = db.query("SELECT COUNT(*) FROM tasks WHERE status='pending'")[0][0]
            self.send_json({"active": active, "completed": completed, "pending": pending})
        elif self.path == "/energy":
            # Real energy logic can be added later, for now we mock it as stable
            self.send_json({"current": 85, "max": 100, "status": "Stable"})
        elif self.path == "/swarm":
            pending = db.query("SELECT COUNT(*) FROM tasks WHERE status='pending'")[0][0]
            self.send_json([{"node": "CORE-01", "energy": 85, "tasks": pending}])
        elif self.path == "/alerts":
            self.send_json([{"level": "INFO", "msg": "System Nominal"}])
        elif self.path == "/stats":
            files = db.query("SELECT COUNT(*) FROM files")[0][0]
            self.send_json({"tracked_files": files, "uptime": "Continuous"})
            
        # 2. Static Assets
        else:
            # Default to index.html
            target = "index.html" if self.path in ["/", "/index.html"] else self.path.lstrip("/")
            file_path = os.path.join(STATIC_DIR, target)
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                if file_path.endswith(".css"): self.send_header("Content-type", "text/css")
                elif file_path.endswith(".js"): self.send_header("Content-type", "text/javascript")
                else: self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

def run(port=8013):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, ProductionDashboardHandler)
    print(f"[*] Command Center Online: http://localhost:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
