import time
import uuid
from dataclasses import dataclass
from cpqa.common import log_d


LOG_TAG = "Scheduler"


@dataclass
class IntervalTask:
    id: str
    task: callable
    interval: int
    next_time: int


class Scheduler:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Scheduler, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__timed_tasks = {}
        self.__ticked_tasks = []
        self.__interval_tasks = []

    def add_after(self, task, delay):
        if delay < 100:
            raise ValueError("delay must be greater than or equal to 100")

        after_time = self.__current_time() + delay
        if self.__timed_tasks.get(after_time) is None:
            self.__timed_tasks[after_time] = []
        self.__timed_tasks[after_time].append(task)

    def add_next_tick(self, task):
        self.__ticked_tasks.append(task)

    def add_interval(self, task, interval):
        task_id = str(uuid.uuid4())
        self.__interval_tasks.append(
            IntervalTask(task_id, task, interval, self.__current_time() + interval)
        )
        return task_id

    def remove_interval(self, task_id):
        for i, task in enumerate(self.__interval_tasks):
            if task.id == task_id:
                del self.__interval_tasks[i]
                return

    def tick(self):
        current_time = self.__current_time()
        # log_d(LOG_TAG, f"current_time: {current_time}")
        for time_key in list(self.__timed_tasks.keys()):
            if time_key <= current_time:
                for task in self.__timed_tasks[time_key]:
                    task()
                del self.__timed_tasks[time_key]

        for task in self.__interval_tasks:
            if task.next_time <= current_time:
                task.task()
                task.next_time = current_time + task.interval

        for task in self.__ticked_tasks:
            task()
        self.__ticked_tasks.clear()

    def __current_time(self):
        return round(time.time() * 1000)
