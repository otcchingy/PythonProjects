from collections import deque


class Stack:
    DATA = deque()

    def __init__(self):
        self.DATA = deque()

    @classmethod
    def push(cls, data):
        cls.DATA.appendleft(data)

    @classmethod
    def pop(cls):
        ret = cls.DATA.popleft()
        return ret

    @classmethod
    def top(cls):
        if cls.isEmpty():
            return None
        return cls.DATA[0]

    @classmethod
    def isEmpty(cls):
        return cls.size() == 0 or cls.DATA is None

    @classmethod
    def size(cls):
        return len(cls.DATA)

    @classmethod
    def __str__(cls):
        return str(cls.DATA)