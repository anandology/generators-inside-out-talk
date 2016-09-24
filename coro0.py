"""Simple conncurrency library using generator-based coroutines.
"""
from collections import deque

_tasks = deque()

def spawn(task):
    _tasks.appendleft(task)
    yield

def run(task):
    _tasks.append(task)
    run_all()

def run_all():
    while _tasks:
        task = _tasks.popleft()
        try:
            next(task)
        except StopIteration:
            pass
        else:
            _tasks.append(task)
