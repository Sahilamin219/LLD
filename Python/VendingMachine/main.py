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