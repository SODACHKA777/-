from datetime import datetime

class Usel():
    def __init__(self, action_id, timestamp, username, action_type):
        self.prev = None
        self.next = None
        self.action_id = action_id
        self.timestamp = timestamp
        self.username = username
        self.action_type = action_type
    
    def __str__(self):
        return f"{self.action_id} {self.timestamp} {self.username} {self.action_type}"
    
    class History():
        def __init__(self):
            self.head=None
            self.tail=None
            self.current=None
            self.action_map={}

        def add_action(self, action_id, timestamp, username, action_type):
            new_usel=Usel(action_id, timestamp, username, action_id)
            if self.head is None:
                self.head = new_usel
                self.tail = new_usel
                self.current = new_usel
            else:
                new_usel.prev = self.current
                new_usel.next = self.current.next
                if self.current.next:
                    self.current.next.prev = new_usel
                    self.current.next = new_usel
                if self.current == self.tail:
                    self.tail = new_usel
                    self.current = new_usel
            self.actions_map[action_id] = new_usel
            
        def undo(self):
            if self.current and self.current.prev:
                self.current=self.current.prev

        def redo(self):
            if self.current and self.current.next:    
                self.current=self.current.next

        def finde_action(self, action_id):
            return self.actions_map.get(action_id, None)
        
        def remove_action(self, action_id):
            usel_to_remove=self.finde_action(action_id)
            if usel_to_remove:
                print(f"Удаляем операцию: {usel_to_remove}")
                if usel_to_remove.prev:
                    usel_to_remove.prev.next = usel_to_remove.next
                if usel_to_remove.next:
                    usel_to_remove.next.prev = usel_to_remove.prev
                if usel_to_remove == self.head:  
                    self.head = usel_to_remove.next
                if usel_to_remove == self.tail:  
                    self.tail = usel_to_remove.prev
                if usel_to_remove == self.current: 
                    self.current = usel_to_remove.prev

                del self.actions_map[action_id]

                current_usel = self.head
                new_id = 1
                while current_usel:
                    current_usel.action_id = new_id
                    self.actions_map[new_id] = current_usel
                    new_id += 1
                    current_usel = current_usel.next

        
        def filret_and_remove(self, action_type):
            current_usel=self.head
            while current_usel:
                if current_usel.action_type==action_type:
                    self.remove_action(current_usel.action_id)
                current_usel=current_usel.next
        
        def __iter__(self):
            current_usel = self.head
            while current_usel:
                yield current_usel
                current_usel = current_usel.next

    def display_history(self):
        for usel in self:
            if usel == self.current:
                print(f"\033[92m{usel}\033[0m")  # Зеленый цвет для текущего
            else:
                print(f"\033[90m{usel}\033[0m")  # Серый цвет для остальных
