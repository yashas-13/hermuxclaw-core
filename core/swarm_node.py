import os
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import sys

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.genetic_engine import GeneticEngine

class SwarmHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/skills":
            pop_file = os.path.expanduser("~/hermuxclaw/memory/population.json")
            if os.path.exists(pop_file):
                with open(pop_file, "r") as f:
                    data = f.read()
            else:
                data = "[]"
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            self.send_response(404)
            self.end_headers()

    # Suppress logging to stdout to prevent noise in ecosystem
    def log_message(self, format, *args):
        pass

class SwarmNode:
    """
    Distributed Swarm Intelligence Node.
    Shares top genomes locally and fetches from peers.
    """
    def __init__(self, port=8000):
        self.port = port
        self.peers = ["127.0.0.1:8000"] # In a real swarm, add other device IPs
        self.engine = GeneticEngine()
        self.server = None
        self.thread = None

    def start_server(self):
        try:
            self.server = HTTPServer(("0.0.0.0", self.port), SwarmHandler)
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            print(f"[🕸️ SWARM] Node listening on port {self.port}")
        except Exception as e:
            print(f"[🕸️ SWARM] Could not start server: {e}")

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def fetch_peer(self, peer_ip):
        try:
            req = urllib.request.Request(f"http://{peer_ip}/skills")
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    return data
        except Exception as e:
            # Silently fail if peer is offline
            pass
        return []

    def sync_swarm(self):
        print(f"\n[🕸️ SWARM] Synchronizing with peers...")
        new_genomes = 0
        for peer in self.peers:
            # Don't sync with self unless testing
            if peer == f"127.0.0.1:{self.port}":
                continue 
                
            peer_skills = self.fetch_peer(peer)
            for skill in peer_skills:
                # Integrate if fitness is high and not already in our population
                if skill.get("fitness", 0) > 0.7:
                    existing = [s for s in self.engine.population if s["id"] == skill["id"]]
                    if not existing:
                        self.engine.add_to_population(
                            skill["name"], 
                            skill["code"], 
                            skill["fitness"], 
                            skill["generation"], 
                            skill["parents"]
                        )
                        new_genomes += 1
                        
        print(f"[🕸️ SWARM] Sync complete. Integrated {new_genomes} foreign genomes.")

if __name__ == "__main__":
    node = SwarmNode()
    node.start_server()
    node.sync_swarm()
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop_server()
