#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import socks
import requests
import time
import os
from getpass import getpass
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.text import Text
import sys

# --- Configuration ---
TOR_PROXY_HOST = '127.0.0.1'
TOR_PROXY_PORT = 9050
TOR_CONTROL_HOST = '127.0.0.1'
TOR_CONTROL_PORT = 9051
IP_CHECK_URL = 'https://api.ipify.org'

# --- UI Elements ---
console = Console()

def print_banner():
    """Prints the main banner."""
    banner_text = """
█████╗ ██╗  ██╗██╗  ██╗███████╗ █████╗ ████████╗
██╔══██╗██║ ██╔╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝
███████║█████╔╝ ███████║███████╗███████║   ██║   
██╔══██║██╔═██╗ ██╔══██║╚════██║██╔══██║   ██║   
██║  ██║██║  ██╗██║  ██║███████║██║  ██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
    """
    console.print(Text(banner_text, style="bold magenta"), justify="center")
    console.print(Panel(Text("Advanced Tor IP Changer", style="bold green"), 
                        title="[bold cyan]Welcome[/bold cyan]", 
                        border_style="green"), justify="center")

def get_current_ip():
    """Gets the current external IP address through the Tor proxy."""
    with Spinner("check", text="Fetching current IP...", style="yellow") as spinner:
        try:
            socks.set_default_proxy(socks.SOCKS5, TOR_PROXY_HOST, TOR_PROXY_PORT)
            socket.socket = socks.socksocket
            response = requests.get(IP_CHECK_URL, timeout=10)
            response.raise_for_status()
            spinner.text = f"Current IP: [bold green]{response.text}[/bold green]"
            spinner.ok("✅")
            return response.text
        except (requests.exceptions.RequestException, socks.ProxyConnectionError) as e:
            spinner.text = f"[bold red]Error fetching IP:[/bold red] {e}"
            spinner.fail("❌")
            return None

def renew_tor_ip(control_password):
    """Sends a signal to the Tor control port to renew the IP."""
    with Spinner("sync", text="Requesting new IP from Tor...", style="cyan") as spinner:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TOR_CONTROL_HOST, TOR_CONTROL_PORT))
                s.send(f'AUTHENTICATE "{control_password}"\r\n'.encode())
                s.send(b'SIGNAL NEWNYM\r\n')
                response = s.recv(1024)
                if b"250 OK" in response:
                    spinner.text = "Successfully requested a new IP."
                    spinner.ok("✅")
                    return True
                else:
                    spinner.text = f"[bold red]Tor control port authentication failed.[/bold red]"
                    spinner.fail("❌")
                    return False
        except Exception as e:
            spinner.text = f"[bold red]Error connecting to Tor control port:[/bold red] {e}"
            spinner.fail("❌")
            return False

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
        console.print("1. Change Tor IP once")
        console.print("2. Auto-change Tor IP at an interval")
        console.print("3. Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")

        if choice == '1':
            control_password = Prompt.ask("[yellow]Enter Tor control password (leave blank if none)[/yellow]", password=True, default="")
            old_ip = get_current_ip()
            if old_ip and renew_tor_ip(control_password):
                console.print("Waiting for the new IP to be assigned...")
                time.sleep(5)
                new_ip = get_current_ip()
                if new_ip and new_ip != old_ip:
                    console.print(f"\n[bold green]IP changed successfully![/bold green]")
                    console.print(f"Old IP: [red]{old_ip}[/red] -> New IP: [green]{new_ip}[/green]")
                else:
                    console.print("[bold yellow]IP did not change. Tor might be slow or unable to find a new circuit.[/bold yellow]")

        elif choice == '2':
            control_password = Prompt.ask("[yellow]Enter Tor control password (leave blank if none)[/yellow]", password=True, default="")
            interval = int(Prompt.ask("Enter interval in seconds", default="60"))
            console.print(f"[cyan]Starting auto IP changer every {interval} seconds. Press Ctrl+C to stop.[/cyan]")
            try:
                while True:
                    old_ip = get_current_ip()
                    if old_ip and renew_tor_ip(control_password):
                        console.print(f"Waiting {interval} seconds before next change...")
                        time.sleep(interval)
                    else:
                        console.print("[bold red]Failed to change IP. Retrying after a short delay...[/bold red]")
                        time.sleep(10)
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Stopping auto IP changer.[/bold yellow]")

        elif choice == '3':
            console.print("[bold yellow]Goodbye![/bold yellow]")
            sys.exit(0)

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Exiting program.[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        console.print("[bold red]Please ensure Tor is installed and running.[/bold red]")
