import os
import sys
import json
import time
import requests
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.align import Align
from rich import box

class HermuxclawTUI:
    """
    High-Performance Terminal Command Center.
    Outperforms standard CLI agents via real-time density and 'Non-Stop' visibility.
    """
    def __init__(self, api_url="http://localhost:8013"):
        self.api_url = api_url
        self.console = Console()
        self.layout = Layout()
        self.start_time = time.time()

    def make_layout(self):
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        self.layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1),
        )
        self.layout["left"].split_column(
            Layout(name="tasks", ratio=2),
            Layout(name="activity", ratio=1),
        )
        self.layout["right"].split_column(
            Layout(name="metrics", ratio=1),
            Layout(name="swarm", ratio=1),
        )

    def get_api_data(self, endpoint):
        try:
            res = requests.get(f"{self.api_url}{endpoint}", timeout=1)
            return res.json()
        except:
            return None

    def generate_header(self):
        energy = self.get_api_data("/energy")
        stats = self.get_api_data("/stats")
        
        status = "[bold green]ONLINE" if energy else "[bold red]OFFLINE"
        energy_str = f"{energy['current']}%" if energy else "--"
        
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            f"[bold blue]HX-CORE[/] [white]v1.5[/]",
            f"[bold white]STATUS:[/] {status}  [bold white]ENERGY:[/] {energy_str}",
            datetime.now().strftime("%H:%M:%S")
        )
        return Panel(grid, style="white on blue", box=box.SQUARE)

    def generate_tasks(self):
        data = self.get_api_data("/tasks")
        table = Table(title="Execution Governance", expand=True, box=box.ROUNDED, border_style="blue")
        table.add_column("Task ID", style="cyan")
        table.add_column("Priority", justify="center")
        table.add_column("Status", justify="right")

        if data:
            table.add_row("System Mapping", "10", f"[green]DONE ({data['completed']})")
            table.add_row("Autonomous Evolution", "25", f"[yellow]PENDING ({data['pending']})")
            table.add_row("Self-Healing Monitor", "30", f"[bold green]ACTIVE ({data['active']})")
        else:
            table.add_row("---", "---", "---")
            
        return table

    def generate_metrics(self):
        energy = self.get_api_data("/energy")
        stats = self.get_api_data("/stats")
        
        content = f"[bold cyan]Intelligence Tier:[/] 1 (Qwen2-0.5B)\n"
        content += f"[bold cyan]Tracked Files:[/] {stats['tracked_files'] if stats else '0'}\n"
        content += f"[bold cyan]Uptime:[/] {stats['uptime'] if stats else '0'}\n"
        
        # Energy Trend Simulation
        trend = "↑ REGENERATING" if energy and energy.get('status') == 'Stable' else "↓ DEPLETING"
        content += f"\n[bold yellow]Energy Trend:[/] {trend}"
        
        return Panel(content, title="Resource Governor", border_style="yellow")

    def generate_activity(self):
        # Simulation of a high-speed log stream (YOLO mode)
        logs = [
            f"[green]✓[/][white] Captured AST node: 'ModelUpgrader'[/]",
            f"[blue]ℹ[/][white] Directing input to Neural Mutator...[/]",
            f"[yellow]⚡[/][white] Tournament Winner: 'echo_service' (0.07s)[/]",
            f"[magenta]🧬[/][white] Evolution Signed in Ledger: {hash(time.time()) % 10000000}[/]"
        ]
        content = "\n".join(logs[-4:])
        return Panel(content, title="Background Activity (Non-Stop)", border_style="green")

    def run(self):
        self.make_layout()
        with Live(self.layout, refresh_per_second=2, screen=True):
            while True:
                self.layout["header"].update(self.generate_header())
                self.layout["tasks"].update(self.generate_tasks())
                self.layout["metrics"].update(self.generate_metrics())
                self.layout["activity"].update(self.generate_activity())
                self.layout["swarm"].update(Panel("HX-CORE-ALPHA: [green]Active[/]\nCompute Swarm: [blue]Optimized[/]", title="Hive State", border_style="magenta"))
                self.layout["footer"].update(Panel("[bold white]DIRECTIVE:[/] [blink]_ [/]", border_style="white"))
                time.sleep(0.5)

if __name__ == "__main__":
    tui = HermuxclawTUI()
    try:
        tui.run()
    except KeyboardInterrupt:
        pass
