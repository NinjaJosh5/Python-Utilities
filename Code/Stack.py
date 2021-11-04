"""
Stack.py

Author: Joshuah Braun || ninjajosh5@gmail.com || 11/4/2021

A class based Stack FILO data structure

"""

class Stack:
    def __init__(self, **kwargs):
        self._stack = []
        ##  max length of queue
        self._max_size = kwargs.get("size", None)
        ##  keep old data and disregard new (True), or remove old data to make room for new (False)
        self._keep_old = kwargs.get("keep_old") if(self._max_size is not None) else False
        ##  semaphore lock
        self._lock = kwargs.get("lock", False)

    # on stack overfill, disregard oldest data
    def push(self, data_element):
        try:
            if(not self.lock):
                if(self._max_size == None or ((self.length +1) < self._max_size) or ((self.length +1) == self._max_size)):
                    self.__put(data_element)
                    return 0
                else:
                    self.__put(data_element)
                    self.__clean()
                    return 0
            else:
                raise Exception("locked")
                return -1
        except Exception:
            return -1

    def __clean(self):
        while(self.length > self._max_size):
            if(self._keep_old):
                self._stack.remove(self._stack[0])
            else:
                self._stack.remove(self._stack[-1])

    def __put(self, data):
        self._stack.insert(0, data)
        return data

    def pop(self):
        if(len(self._stack) > 0):
            val = self._stack[0]
            self._stack.remove(val)
            return val
        else:
            return None

    def peek(self):
        if(len(self._stack) > 0):
            val = self._stack[0]
            return val
        else:
            return None

    def __str__(self):
        stringy = ""
        for i in range(len(self._stack)-1):
            stringy += str(self._stack[i])
            stringy += " -> "
        stringy += str(self._stack[-1])
        return stringy

    @property
    def length(self):
        return len(self._stack)

    @property
    def lock(self):
        return self._lock

    @lock.setter
    def lock(self, status:bool):
        self._lock = status

