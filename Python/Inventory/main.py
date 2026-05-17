"""
Requirements:
1. Track inventory for products across multiple warehouses
2. Add stock to a specific warehouse (receiving shipments)
3. Remove stock from a specific warehouse (fulfilling orders)
4. Check availability: given a product and quantity, return which warehouses can fulfill it
5. Transfer stock between warehouses
6. Low-stock alerts
7. Reject operations that would result in negative inventory
8. System must be thread-safe to handle concurrent operations -> concurrent hashmap

Out of Scope:
- Product catalog management (products exist externally)
- Order processing / payment / serviceability
- Persistence
"""

# Entities
# WareHouseOrch
#     - Warehouse (list)
#     + add 
#     + remove
#     + transfer (id1, id2, pid, count) -> add / remove

# Warehouse
#     - id
#     - product(list)
#     - productCount # hashmap
#     + add/remove

# Product
#     - pid

# ProductStatus
#     + check 
