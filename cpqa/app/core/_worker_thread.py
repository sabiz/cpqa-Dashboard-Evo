from threading import Thread
from threading import Event
from threading import main_thread
from queue import Queue
from queue import Empty as QueueEmpty
from cpqa.common import log_e

LOG_TAG = "WorkerThread"


class WorkerThread(Thread):
    def __init__(self):
        super().__init__()
        self.__queue = Queue()
        self.__stop_event = Event()

    def run(self):
        while not self.__stop_event.is_set() and main_thread().is_alive():
            try:
                task, args = self.__queue.get(timeout=1)
                try:
                    task(*args)
                except Exception as e:
                    log_e(LOG_TAG, f"task failed: {e}")
            except QueueEmpty:
                pass

    def stop(self):
        self.__stop_event.set()
        self.join()

    def add_task(self, task, *args):
        self.__queue.put((task, args))
