import time
from cpqa.app.core import Scheduler


def test_add_after():
    x = 0

    def f():
        nonlocal x
        x = 1

    scheduler = Scheduler()
    scheduler.add_after(f, 1000)
    assert len(scheduler._Scheduler__timed_tasks) == 1
    time.sleep(1)
    scheduler.tick()
    assert x == 1
    assert len(scheduler._Scheduler__timed_tasks) == 0


def test_add_next_tick():
    x = 0

    def f():
        nonlocal x
        x = 1

    scheduler = Scheduler()
    scheduler.add_next_tick(f)
    assert len(scheduler._Scheduler__ticked_tasks) == 1
    scheduler.tick()
    assert x == 1
    assert len(scheduler._Scheduler__ticked_tasks) == 0


def test_add_interval():
    x = 0

    def f():
        nonlocal x
        x += 1

    scheduler = Scheduler()
    task_id = scheduler.add_interval(f, 1000)
    assert len(scheduler._Scheduler__interval_tasks) == 1
    time.sleep(1)
    scheduler.tick()
    assert x == 1
    assert len(scheduler._Scheduler__interval_tasks) == 1
    time.sleep(1)
    scheduler.tick()
    assert x == 2
    assert len(scheduler._Scheduler__interval_tasks) == 1
    scheduler.remove_interval(task_id)
    assert len(scheduler._Scheduler__interval_tasks) == 0
