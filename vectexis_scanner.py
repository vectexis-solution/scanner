import argparse
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def banner():
    title = Text("Vectexis Scanner", style="bold cyan")
    body = Text()
    body.append("Powered by ", style="dim")
    body.append("Vectexis Solution\n", style="bold white")
    body.append("LinkedIn: https://linkedin.com/company/vectexis-solution\n", style="blue")
    body.append("GitHub: https://github.com/vectexis-solution", style="blue")

    console.print(Panel(body, title=title, border_style="cyan", padding=(1, 2)))

def save_output(content: str, path: str):
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        console.print(f"[green][+][/green] Output saved to [bold]{p.resolve()}[/bold]")
    except Exception as e:
        console.print(f"[red][!][/red] Failed to save output: {e}")

# --- scan ---
def do_scan(target, port, output=None, fast=False):
    console.print(f"[bold yellow][*] Scanning...[/bold yellow] {target} on port(s) {port}")

    cmd = ["nmap", "-v"]
    cmd.append("-F" if fast else "-A")
    cmd.extend(["-p", port, target])

    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        console.print(result.stdout)

        full_output = f"--- Vectexis Scanner ---\nTarget: {target}\nPorts: {port}\nDate: {datetime.now()}\nCommand: {' '.join(cmd)}\n\n{result.stdout}\n{result.stderr}"

        if output:
            save_output(full_output, output)
        elif result.stderr:
            console.print(f"[red]{result.stderr}[/red]", file=sys.stderr)

    except FileNotFoundError:
        console.print("[red][!] nmap not found. Install nmap first.[/red]")
    except subprocess.TimeoutExpired:
        console.print("[red][!] Scan timed out after 600s[/red]")
    except Exception as e:
        console.print(f"[red][!] Error: {e}[/red]")

# --- Crawl ---
def do_crawl(url, output=None):
    console.print(f"[bold yellow][*] Crawling...[/bold yellow] {url}")
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else "No Title"
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

        console.print(f"[green][+][/green] Title: [bold]{title}[/bold]")
        console.print(f"[green][+][/green] Fetched {len(response.text)} chars, Found {len(links)} links")

        for link in links[:50]: # print first 50
            console.print(f" - {link}")
        if len(links) > 50:
            console.print(f"[dim]... and {len(links)-50} more[/dim]")

        if output:
            content = f"--- Vectexis Crawler ---\nURL: {url}\nDate: {datetime.now()}\nTitle: {title}\n\nLinks:\n" + "\n".join(links)
            save_output(content, output)

    except Exception as e:
        console.print(f"[red][!] Error: {e}[/red]")

# --- Parser ---
parser = argparse.ArgumentParser(description="Vectexis Scanner - Powered by Vectexis Solution")
sub = parser.add_subparsers(dest="cmd", required=True)

scan = sub.add_parser("scan", help="Run a nmap scan")
scan.add_argument("-t", "--target", required=True, help="target ip / hostname")
scan.add_argument("-p", "--port", default="1-1000", help="port(s) e.g. 80, 1-1000 (default: 1-1000)")
scan.add_argument("-o", "--output", help="save output to file e.g. report.txt")
scan.add_argument("--fast", action="store_true", help="use fast scan (-F) instead of -A")

crawl = sub.add_parser("crawl", help="crawl a page")
crawl.add_argument("url", help="URL to crawl")
crawl.add_argument("-o", "--output", help="save output to file")

args = parser.parse_args()

banner()

if args.cmd == "scan":
    do_scan(args.target, args.port, args.output, args.fast)
elif args.cmd == "crawl":
    do_crawl(args.url, args.output)