from collections import deque

class MyQueue:
    def __init__(self):
        self.queue = deque()

    def put(self, item):
        self.queue.appendleft(item)

    def get(self):
        return self.queue.pop()

    def empty(self):
        return not self.queue