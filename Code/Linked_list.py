class Node:
    def __init__(self, **kwargs):
        self.value = kwargs.get('value', None)
        self.nextval = kwargs.get('next', None)

class LinkedList:
    def __init__(self, **kwargs):
        self.start : Node = kwargs.get('head', None)
    
    def insert(self, location_node:Node, new_node:Node):
        temp_next = location_node.nextval
        location_node.nextval = new_node
        new_node.nextval = temp_next

    def last_node(self):
        current = self.start
        while current.nextval is not None:
            current = current.nextval
        return current

    def count(self):
        current = self.start
        count = 0
        while current.nextval is not None:
            current = current.nextval
            count += 1
        return count +1

    def insert_start(self, new_node:Node):
        temp = self.start
        self.start = new_node
        self.start.nextval = temp.nextval
        temp.nextval = self.start
        self.insert(self.start, temp)

    def __str__(self):
        stringy = ""
        current = self.start
        while current is not None:
            stringy += f"{current.value} -> " if(current.nextval is not None) else f"{current.value}"
            current = current.nextval
        return stringy
