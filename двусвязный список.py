class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

    def __repr__(self):
        return str(self.value)


class DoubleLinkedList:
    def __init__(self, cycle=False):
        self.head = None
        self.tail = None
        self.length = 0
        self.cycle = cycle

    def __str__(self):
        if self.length == 0:
            return "Empty List"
        result = []
        current = self.head
        while True:
            result.append(str(current.value))
            current = current.next
            if current == self.head or current is None:
                break
        return " <-> ".join(result)

    def add_to_start(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        if self.cycle:
            self._make_cyclic()
        self.length += 1

    def add_to_end(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = self.tail = new_node
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node
        if self.cycle:
            self._make_cyclic()
        self.length += 1

    def add_at_index(self, index, value):
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")
        if index == 0:
            self.add_to_start(value)
        elif index == self.length:
            self.add_to_end(value)
        else:
            new_node = Node(value)
            current = self._get_node(index)
            prev_node = current.previous
            prev_node.next = new_node
            new_node.previous = prev_node
            new_node.next = current
            current.previous = new_node
            self.length += 1

    def remove_from_start(self):
        if self.length == 0:
            raise IndexError("List is empty")
        removed_value = self.head.value
        if self.length == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.previous = None
        if self.cycle:
            self._make_cyclic()
        self.length -= 1
        return removed_value

    def remove_from_end(self):
        if self.length == 0:
            raise IndexError("List is empty")
        removed_value = self.tail.value
        if self.length == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.previous
            self.tail.next = None
        if self.cycle:
            self._make_cyclic()
        self.length -= 1
        return removed_value

    def remove_at_index(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        if index == 0:
            return self.remove_from_start()
        if index == self.length - 1:
            return self.remove_from_end()
        current = self._get_node(index)
        prev_node = current.previous
        next_node = current.next
        prev_node.next = next_node
        next_node.previous = prev_node
        self.length -= 1
        return current.value

    def remove_all_occurrences(self, value):
        count_removed = 0
        current = self.head
        while current:
            if current.value == value:
                if current == self.head:
                    self.remove_from_start()
                elif current == self.tail:
                    self.remove_from_end()
                else:
                    prev_node = current.previous
                    next_node = current.next
                    prev_node.next = next_node
                    next_node.previous = prev_node
                    self.length -= 1
                    count_removed += 1
                current = current.next if current != self.head else self.head
            else:
                current = current.next if current != self.tail else self.tail
        return count_removed

    def _make_cyclic(self):
        if self.length > 0:
            self.head.previous = self.tail
            self.tail.next = self.head

    def _get_node(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next
            if current == self.head:
                break

    def get_by_index(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        return self._get_node(index).value

    def reverse(self):
        reversed_list = DoubleLinkedList(cycle=self.cycle)
        current = self.tail
        while current:
            reversed_list.add_to_end(current.value)
            current = current.previous
            if current == self.tail:
                break
        return reversed_list
