"""
Requirements
user can insert coin/notes
user can pick items
user can buy single/multiple items
maintain invetory for vending machine
if item not present let user know

"""

class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0
"""entities
pacakge 
    - versionHistory
    - name
    - current
    - depencencies -> pacakges : list
    + checkCylcle()

version
    - string
    + comparator()


ticketnumber
url
airline system

text editor 
enties:

 class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
    
    def __repr__(self):
        return f"({self.key} : {self.value})"

class LRUCache:

    def __init__(self, capacity: int):
        self.size = capacity
        self.cur_size = 0
        self.head = -1
        self.last = self.head
        self.map = dict()
        
        self.map[self.head] = Node(self.head, -1)
        
    def pop(self):
        if self.cur_size > 0:
            head_node = self.map[self.head]
            first_node = head_node.next
            
            self.remove(first_node.key)
            
    
    def remove(self,key):
        node = self.map[key]
        
        prev = node.prev
        nex  = node.next
        
        prev.next = nex
        if nex: nex.prev = prev
        
        if key == self.last: self.last = prev.key
        
        self.map.pop(key)
        self.cur_size -= 1
        
        return node
    
    def append(self,node):
        node.next = None
        node.prev = None
        
        last_node = self.map[self.last]
        
        last_node.next = node
        node.prev = last_node
        node.next = None
        
        self.last = node.key
        self.map[node.key] = node
        self.cur_size += 1
        

    def get(self, key: int) -> int:
        ans = -1
        if key in self.map:
            node = self.remove(key)
            ans = node.value
            self.append(node)
        return ans
        

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self.remove(key)
        elif (key not in self.map) and self.cur_size >= self.size:
            self.pop()
        node = Node(key, value)
        self.append(node)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)"""

# Pizza LLD using Decorator Design Pattern
from abc import ABC, abstractmethod


class Pizza(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class Margherita(Pizza):
    def get_description(self) -> str:
        return "Margherita"

    def get_cost(self) -> float:
        return 8.0


class Farmhouse(Pizza):
    def get_description(self) -> str:
        return "Farmhouse"

    def get_cost(self) -> float:
        return 10.0


class PizzaDecorator(Pizza):
    def __init__(self, pizza: Pizza) -> None:
        self.pizza = pizza

    def get_description(self) -> str:
        return self.pizza.get_description()

    def get_cost(self) -> float:
        return self.pizza.get_cost()


class ExtraCheese(PizzaDecorator):
    def get_description(self) -> str:
        return f"{self.pizza.get_description()} + Extra Cheese"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.5


class Olives(PizzaDecorator):
    def get_description(self) -> str:
        return f"{self.pizza.get_description()} + Olives"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.0


class Mushrooms(PizzaDecorator):
    def get_description(self) -> str:
        return f"{self.pizza.get_description()} + Mushrooms"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.2


def print_order(title: str, pizza: Pizza) -> None:
    print(f"{title}: {pizza.get_description()} | Total = ${pizza.get_cost():.2f}")


if __name__ == "__main__":
    # Base pizza
    order_1 = Margherita()
    print_order("Order 1", order_1)

    # Decorated pizza
    order_2 = ExtraCheese(Olives(Margherita()))
    print_order("Order 2", order_2)

    # Another combination
    order_3 = Mushrooms(ExtraCheese(Farmhouse()))
    print_order("Order 3", order_3)

class Singleton:
    instance = None
    initialized = False # Flag to prevent re-initialization on subsequent calls

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            # You can call the initializer here if needed
        return cls.instance

    def __init__(self, some_value=None):
        if not self.initialized:
            self.value = some_value
            Singleton.initialized = True
            print("Instance initialized only once")
        else:
            print("Instance already initialized, skipping init")


# Client code
s1 = Singleton(some_value="First Value")
s1 = Singleton(some_value="First Value")

s2 = Singleton(some_value="Second Value") # __init__ is called again, but initialization logic skipped

print(s1 is s2) # Output: True
print(f"S1 value: {s1.value}") # Output: S1 value: First Value
print(f"S2 value: {s2.value}") # Output: S2 value: First Value
import threading
import time

def do_something(seconds):
    print(f"Sleeping for {seconds} second(s)...")
    time.sleep(seconds) # Simulates an I/O-bound operation
    print("Done sleeping in thread.")

t1 = threading.Thread(target=do_something, args=(2,))
t2 = threading.Thread(target=do_something, args=(1,))

t1.start()
t2.start()

t1.join() # Wait for t1 to finish
t2.join() # Wait for t2 to finish

print("Main thread finished.")
import asyncio

async def greet(name, delay):
    print(f"Hello, {name}! Starting to sleep for {delay} seconds.")
    await asyncio.sleep(delay) # Hands control back to the event loop
    print(f"Goodbye, {name}! Done sleeping.")

async def main():
    # Create tasks to run concurrently
    task1 = asyncio.create_task(greet("Alice", 2))
    task2 = asyncio.create_task(greet("Bob", 1))

    # Wait for both tasks to complete
    await task1
    await task2

asyncio.run(main())
import asyncio
import time

def blocking_sync_function():
    """A normal synchronous function that blocks."""
    time.sleep(2)
    return "Result from blocking function"

async def main():
    print("Starting blocking function in a thread...")
    result = await asyncio.to_thread(blocking_sync_function) # Offload to a thread
    print(f"Received: {result}")

asyncio.run(main())
 