import time
from cpqa.app.core import WorkerThread


def test_worker_thread():
    x = 0

    def f(v):
        nonlocal x
        x = v

    worker_thread = WorkerThread()
    worker_thread.start()
    worker_thread.add_task(f, 1)
    time.sleep(1)
    worker_thread.stop()
    assert x == 1
