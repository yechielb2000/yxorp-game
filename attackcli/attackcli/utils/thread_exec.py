import threading
from queue import Queue, Empty
import typer


class ThreadedExecutor:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.tasks = Queue()
        self.threads = []
        self._stop_event = threading.Event()

    def submit(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def _worker(self):
        while not self._stop_event.is_set():
            try:
                func, args, kwargs = self.tasks.get(timeout=0.5)
            except Empty:
                continue

            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Task error: {e}")
            finally:
                self.tasks.task_done()

    def start(self):
        with typer.progressbar(range(self.max_workers), label="Starting workers") as progress:
            for _ in progress:
                t = threading.Thread(target=self._worker)
                t.start()  # Removed daemon=True
                self.threads.append(t)

    def wait(self):
        typer.echo(typer.style("[+] Stopping...", fg=typer.colors.MAGENTA))
        typer.echo(typer.style("[+] Waiting for tasks to complete...", fg=typer.colors.MAGENTA))
        typer.echo(typer.style("[+] To stop immediately Ctrl + C again", fg=typer.colors.MAGENTA))
        self.tasks.join()
        self._stop_event.set()
        for t in self.threads:
            t.join()
        typer.echo(typer.style("[+] All tasks submitted!", fg=typer.colors.GREEN))
