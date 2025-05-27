import typer
from typer import colors

from http_strike_kit.attacks import (
    syn_flood_attack,
    brute_force_attack,
    slowloris_attack
)

app = typer.Typer()
attacks_app = typer.Typer(help="Attack commands")


@attacks_app.command()
def syn_flood(
        target: str = typer.Option(..., "-t", "--target", help="Target IP or hostname"),
        port: int = typer.Option(80, "-p", "--port", help="Target port"),
        threads: int = typer.Option(500, "-w", "--threads", help="Number of concurrent threads"),
):
    typer.echo(typer.style(f"[+] Starting SYN flood on {target}:{port} with {threads} threads", fg=colors.MAGENTA))
    syn_flood_attack(target, port, threads)
    typer.echo(typer.style("[+] Done", fg=typer.colors.GREEN))


@attacks_app.command()
def brute_force(
        base_url: str = typer.Option(..., "-u", "--base-url", help="Base URL to target"),
        wordlist_path: str = typer.Option(..., "-w", "--wordlist", help="Path to the wordlist"),
        workers: int = typer.Option(100, "-t", "--workers", help="Number of concurrent workers"),
):
    typer.echo(typer.style(f"[+] Starting Brute Force attack on {base_url} with {workers} workers.", fg=colors.MAGENTA))
    brute_force_attack(base_url, wordlist_path, workers)
    typer.echo(typer.style("[+] Done", fg=typer.colors.GREEN))


@attacks_app.command()
def slowloris(
        target: str = typer.Option(..., "-t", "--target", help="Target IP or hostname"),
        port: int = typer.Option(..., "-p", "--port", help="Target port"),
        timeout: float = typer.Option(10.0, "-o", "--timeout", help="Socket timeout in seconds"),
        workers: int = typer.Option(100, "-w", "--workers", help="Number of concurrent workers"),
):
    typer.echo(
        typer.style(f"[+] Starting Slow loris attack on {target}:{port} with {workers} workers.", fg=colors.MAGENTA))
    slowloris_attack(target, port, timeout, workers)
    typer.echo(typer.style("[+] Done", fg=typer.colors.GREEN))


if __name__ == "__main__":
    app.add_typer(attacks_app, name="attack")
    app()
