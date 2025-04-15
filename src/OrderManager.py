## OrderManager.py
## Manages restaurant orders, including creation, retrieval, and updates.

from Order import Order
from Dish import Dish

class OrderManager: 
    # constructor, Initializes empty list of orders and counters.     
    def __init__(self):
        self.__orders = []
        self.__created_orders_num = 0  # Total number of orders ever created. 
        self.__stored_orders_num = 0   # Number of stored orders in the list.
        self.__active_orders_num = 0   # Number of currently active orders.

    @property
    def created_orders_num(self):
        return self.__created_orders_num
      
    @property
    def stored_orders_num(self):
        return self.__stored_orders_num

    @property
    def active_orders_num(self):
        return self.__active_orders_num

    @property
    def orders(self):
        return self.__orders 
    
    # Returns the total price of an order by table number.
    def get_order_price(self, table_number):
        order = self.find_order("table",table_number)
        return order.get_total_price()  

    # Returns the status of an order by table number.
    def get_order_status(self, table_number):
        order = self.find_order("table",table_number)
        return order.status

    # Returns customer name for a given table number.
    def get_customer_name(self, table_number):
        order = self.find_order("table",table_number)
        return order.customer_name

    # Updates the customer name for a given table number.
    def change_customer_name(self, table_number, name):
        order = self.find_order("table",table_number)
        order.customer_name = name
        
    # Returns the price of a dish in a specific order.
    def get_dish_price(self, table_number, dish_name):
        order = self.find_order("table",table_number)
        return order.get_dish_price(dish_name)

    # Returns the status of a dish in a specific order.
    def get_dish_status(self, table_number, dish_name):
        order = self.find_order("table",table_number)
        return order.get_dish_status(dish_name)
    
    # Validates the identifier type and value before searching for an order.
    def check_valid_identifier(self, identi_type, identi_value):
        if identi_type is None or identi_value is None:
           raise ValueError("identifier details cannot be None")
        if not isinstance(identi_type, str):
           raise TypeError("identifier type must be a string")
        identi_type = identi_type.lower().strip()   
        if identi_type not in {"table", "id", "customer"}:
           raise ValueError("identifier type must be 'table' or 'id' or 'customer'.")
       
        if identi_type == "customer":
           if not isinstance(identi_value, str):
              raise TypeError("identifier value must be a string")
           identi_value = identi_value.strip()  
           if not identi_value:   
              raise ValueError("identifier value cannot be empty")   
        identi_value = int(identi_value)  
        if identi_value <= 0:
           raise ValueError("identifier value must be positive")
             
    # Finds and returns an order based on the given identifier.
    def find_order(self, identifier_type, identifier_value):
        self.check_valid_identifier(identifier_type, identifier_value) 
        for order in self.orders:  
            if getattr(order, identifier_type) == identifier_value:
                if identifier_type != "table":
                   return order
                if order.status != "Done":
                   return order
        raise LookupError("Order is not found")
  
    # Adds a new order to the system, assigning it a unique ID and updating counters.
    def add_order(self, order):
        self.created_orders_num += 1 
        self.stored_orders_num += 1
        self.active_orders_num += 1 
        order.id = self.created_orders_num
        self.orders.append(order)

    # Removes an order from the system based on an identifier (table, ID, or customer) and updating counters.
    def remove_order(self, identifier_type, identifier_value):
        order = self.find_order(identifier_type, identifier_value)
        self.orders.remove(order)
        self.stored_orders_num -= 1
        self.active_orders_num -= 1

    # Marks an order as 'Done', update active orders counter
    # and return the total price of the order.  
    def close_order(self, table_number):
        order = self.find_order("table",table_number)
        order.status = "Done"      
        self.active_orders_num -= 1
        return order.get_total_price()

    # Adds a dish to an existing order.
    def add_dish_to_order(self, table_number, dish: Dish):
        order = self.find_order("table",table_number)
        order.add_dish(dish)

    # Removes a dish from an order. if the order became empty- order deleted.
    def remove_dish_from_order(self, table_number, dish_name):
        order = self.find_order("table", table_number)
        order.remove_dish(dish_name)
        if not order.dishes:
           self.remove_order("table", table_number) 

    # Updates the quantity of a specific dish in an order.
    def update_dish_quantity(self, table_number, dish_name, new_quantity):
        order = self.find_order("table",table_number)
        order.update_dish_quantity(dish_name, new_quantity)

    # Updates the status of a dish within an order.   
    def update_dish_status(self, table_number, dish_name, status):
        order = self.find_order("table",table_number)
        order.update_dish_status(dish_name, status)

    # Validates the order status before processing.
    def check_valid_status(self, status):
        if status is None:
           raise ValueError("status cannot be None")
        if not isinstance(status, str):
           raise TypeError("status must be a string")
        if status not in {"Pending", "Served", "Done", "all"}:
           raise ValueError("status is not valid")

    # Returns a list of table numbers with orders matching a given status.
    def get_table_numbers_by_order_status(self,status):
        self.check_valid_status(status)
        if status == "all":
           raise ValueError("status cannot be 'all'")
        return [order.table_number for order in self.orders if order.status == status]

    # Calculates the total price of all orders matching a given status.
    # If status is 'all', returns the total price of all orders.
    def total_orders_price_by_status(self, status):
        self.check_valid_status(status)
        if status == "all":
           return sum(order.get_total_price() for order in self.orders)
        return sum(order.get_total_price() for order in self.orders if order.status == status)    

    # Retrieves all dishes in an order that match a given status.
    def get_table_dishes_by_status(self, table_number, status):
        order = self.find_order("table",table_number) 
        return order.get_dishes_by_status(status)

    # Returns a list of all dishes across all orders that match a given status.
    def get_all_dishes_by_status(self, status):
        dishes = []
        for order in self.orders:
            dishes.extend(order.get_dishes_by_status(status))
        return dishes
   
    # Converts the order manager's data into a dictionary format for serialization.
    def to_dict(self):
        return {
        "created_orders_num": self.created_orders_num,
        "stored_orders_num": self.stored_orders_num,
        "active_orders_num": self.active_orders_num,
        "orders": [order.to_dict() for order in self.orders]
        }
