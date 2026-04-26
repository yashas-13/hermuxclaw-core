import os
import sys
import json
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser

WORKSPACE = os.path.expanduser("~/hermuxclaw")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hermuxclaw Architecture Dashboard</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #fff; }
        #network-container { width: 100vw; height: 100vh; }
        #panel { position: absolute; top: 20px; left: 20px; background: rgba(30, 41, 59, 0.9); padding: 20px; border-radius: 8px; border: 1px solid #334155; max-width: 350px; z-index: 10; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { margin: 0 0 10px 0; font-size: 1.2rem; color: #38bdf8; }
        .stat { margin: 5px 0; font-size: 0.9rem; color: #cbd5e1; }
        .legend-item { display: flex; align-items: center; margin-top: 5px; font-size: 0.85rem; }
        .color-box { width: 12px; height: 12px; margin-right: 8px; border-radius: 2px; }
        button { background: #0284c7; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-top: 15px; width: 100%; font-weight: bold; }
        button:hover { background: #0369a1; }
    </style>
</head>
<body>
    <div id="panel">
        <h1>🧠 Hermuxclaw Live Architecture</h1>
        <div class="stat" id="node-count">Nodes: Loading...</div>
        <div class="stat" id="edge-count">Edges: Loading...</div>
        <div style="margin-top: 15px; font-weight: bold; font-size: 0.9rem;">Layer Legend</div>
        <div class="legend-item"><div class="color-box" style="background: lightblue;"></div> Entry</div>
        <div class="legend-item"><div class="color-box" style="background: lightsalmon;"></div> Core</div>
        <div class="legend-item"><div class="color-box" style="background: lightgray;"></div> Utility</div>
        <button onclick="fetchData()">🔄 Refresh Map</button>
    </div>
    <div id="network-container"></div>

    <script>
        var network = null;

        function fetchData() {
            fetch('/architecture.dot')
                .then(response => response.text())
                .then(dotData => {
                    var parsedData = vis.parseDOTNetwork(dotData);
                    
                    var data = {
                        nodes: parsedData.nodes,
                        edges: parsedData.edges
                    };

                    document.getElementById('node-count').innerText = 'Nodes: ' + data.nodes.length;
                    document.getElementById('edge-count').innerText = 'Edges: ' + data.edges.length;

                    var options = {
                        nodes: {
                            shape: 'box',
                            font: { color: '#0f172a', face: 'monospace' },
                            borderWidth: 2,
                            shadow: true
                        },
                        edges: {
                            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
                            color: { color: '#475569', highlight: '#38bdf8' },
                            smooth: { type: 'cubicBezier', forceDirection: 'none', roundness: 0.4 }
                        },
                        physics: {
                            barnesHut: { gravitationalConstant: -30000, centralGravity: 0.3, springLength: 150, springConstant: 0.04 },
                            stabilization: { iterations: 150 }
                        },
                        interaction: { hover: true, tooltipDelay: 200 }
                    };

                    var container = document.getElementById('network-container');
                    
                    if (network !== null) {
                        network.destroy();
                        network = null;
                    }
                    
                    network = new vis.Network(container, data, options);
                })
                .catch(err => {
                    console.error("Failed to fetch DOT graph:", err);
                    document.getElementById('node-count').innerText = 'Error loading map';
                });
        }

        // Auto-refresh every 30 seconds
        setInterval(fetchData, 30000);
        fetchData();
    </script>
</body>
</html>
"""

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=MEMORY_DIR, **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode())
        else:
            # Serve files from memory dir (like architecture.dot)
            super().do_GET()

    def log_message(self, format, *args):
        pass # Suppress logs

def run_server(port=8080):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"[*] 📊 Live Architecture Dashboard running at http://localhost:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
