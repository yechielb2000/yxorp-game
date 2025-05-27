import requests
import typer

from http_strike_kit.utils.thread_exec import ThreadedExecutor


def _send_get_request(base_url: str, path: str, desired_statues: list[int]):
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    try:
        response = requests.get(url, timeout=2)
        if response.status_code in desired_statues:
            message = f"[+] Found: {url} (Status: {response.status_code})"
            typer.echo(typer.style(message, fg=typer.colors.GREEN, bold=True))
        else:
            message = f"[+] Url: {url} (Status: {response.status_code})"
            typer.echo(typer.style(message, fg=typer.colors.BRIGHT_BLACK))
    except requests.RequestException:
        typer.echo(typer.style(f"[+] Error while sending request!", fg=typer.colors.RED, bold=True))


def brute_force_attack(base_url: str, wordlist_path: str, workers: int, desired_statues: list[int]):
    with open(wordlist_path, "r") as f:
        paths = [line.strip() for line in f if line.strip()]

    executor = ThreadedExecutor(max_workers=workers)
    executor.start()

    for path in paths:
        executor.submit(_send_get_request, base_url, path, desired_statues)

    executor.wait()
