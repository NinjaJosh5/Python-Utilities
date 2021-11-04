"""
Queue.py

Author: Joshuah Braun || ninjajosh5@gmail.com || 11/4/2021

A class based Queue FIFO data structure

"""

class Queue:
    def __init__(self, **kwargs):
        self._queue = []
        ##  max length of queue, can be null
        self._max_size = kwargs.get("size", None)
        ##  keep old data and disregard new (True), or remove old data to make room for new (False)
        self._keep_old = kwargs.get("keep_old") if(self._max_size is not None) else False
        ##  semaphore lock - True is locked
        self._lock = kwargs.get("lock", False)

    def push(self, data_element):
        try:
            if(not self._lock):
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

    ##  add data element to structure
    def __put(self, data):
        self._queue.append(data)
        return data
    
    def __clean(self):
        while(self.length > self._max_size):
            if(self._keep_old):
                self._queue.remove(self._queue[-1])
            else:
                self._queue.remove(self._queue[0])

    def pop(self):
        if(len(self._queue) > 0):
            val = self._queue[0]
            self._queue.remove(val)
            return val
        else:
            return None
    
    ##  access next element without dequeuing 
    def peek(self):
        if(len(self._queue) > 0):
            val = self._queue[0]
            return val
        else:
            return None

    def __str__(self):
        stringy = ""
        for i in range(len(self._queue)-1):
            stringy += str(self._queue[i])
            stringy += " -> "
        stringy += str(self._queue[-1])
        return stringy

    @property
    def length(self):
        return len(self._queue)

    @property
    def lock(self):
        return self._lock

    @lock.setter
    def lock(self, status:bool):
        self._lock = status
