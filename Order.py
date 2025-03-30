## Order.py
## Represents a restaurant order associated with a specific table.
## Manages dishes, customer details, and order status.

from Dish import Dish
class Order:

    # constructor- start with empty list of dishes, id will change later,
    # Default status is 'Served' (no pending dishes).
    def __init__(self, customer_name, table_number):
        self.id = 1
        self.customer_name = customer_name
        self.table_number = table_number
        self.dishes = []  
        self.status = "Served"

    @property
    def id(self):
        return self.__id

    # Sets the order ID, ensuring it is a positive integer.
    @id.setter
    def id(self, id):
        self.check_valid_num_identifier(id, "id") 
        self.__id = id

    @property
    def customer_name(self):
        return self.__customer_name

    # Sets the customer name, ensuring it is a non-empty string.
    @customer_name.setter
    def customer_name(self, name):
        self.check_valid_name(name)
        self.__customer_name = name

    @property
    def table_number(self):
        return self.__table_number

    # Sets the table number, ensuring it is a positive integer.
    @table_number.setter
    def table_number(self, table_number):
        self.check_valid_num_identifier(table_number, "table number")
        self.__table_number = table_number

    @property
    def dishes(self):
        return self.__dishes

    @property
    def status(self):
        return self.__status

    # check if table number or order id are validate
    def check_valid_num_identifier(self, number, identi_type):
        if number is None:
           raise ValueError(f"{identi_type} cannot be None")
        if not isinstance(number, int):
           raise TypeError(f"{identi_type} must be a integer")
        if number <= 0:
           raise ValueError(f"{identi_type} must be positive")

    # check if dish name or customer name are validate
    def check_valid_name(self, name):
        if name is None:
           raise ValueError("name cannot be None")
        if not isinstance(name, str):
           raise TypeError("name must be a string")
        name = name.strip()  
        if not name:
           raise ValueError("name cannot be empty")
        
    # Sets the order status. Must be 'Pending', 'Served', or 'Done'.
    @status.setter
    def status(self, status):
        self.check_valid_status(status)
        if status not in {"Pending", "Served", "Done"}:
           raise ValueError("status must be 'Pending' or 'Served' or 'Done'")
        self.__status = status

    # Finds and returns a dish by name. Raises an error if not found.
    def find_dish_by_name(self, dish_name):
        self.check_valid_name(dish_name)
        for dish in self.dishes:
            if dish.name == dish_name:
               return dish
        raise LookupError (f"{dish_name} is not found in that order")

    # Returns dish price by the name of the dish.
    def get_dish_price(self, dish_name):
        dish = self.find_dish_by_name(dish_name)
        return dish.price  

    # Returns dish status by the name of the dish.
    def get_dish_status(self, dish_name):
        dish = self.find_dish_by_name(dish_name)
        return dish.status

    # Checks if a dish exists in the order.
    def is_dish_exists_in_order(self, dish_name):
        self.check_valid_name(dish_name)
        for dish in self.dishes:
            if dish.name == dish_name:
               return True
        return False     

    # Adds a dish to the order if it doesn't already exist.
    def add_dish(self, dish: Dish):
        if self.is_dish_exists_in_order(dish.name):
           raise ValueError(f"the dish '{dish.name}' is already exists in the order.")
        dish.status = "Pending"  # New dish starts as Pending
        self.dishes.append(dish)  
        self.status = "Pending"  # Adding a dish sets the order to Pending

    # Removes a dish from the order and updates the order status.
    def remove_dish(self, dish_name):
        dish = self.find_dish_by_name(dish_name)
        self.dishes.remove(dish)
        self.check_order_status()  

    # Updates the order status based on the statuses of its dishes.
    # if all the dishes Served- the order is Served.
    def check_order_status(self):
        for dish in self.dishes:
            if dish.status == "Pending":
                self.status = "Pending"
                return 
        self.status = "Served"
  
    # Updates dish quantity and adjusts its status if needed.
    def update_dish_quantity(self, dish_name, quantity):
        self.check_valid_num_identifier(quantity, "quantity")
        dish = self.find_dish_by_name(dish_name)
        if dish.quantity < quantity:
           dish.status = "Pending"  # Increasing quantity resets status to Pending
           self.status = "Pending"
        dish.quantity = quantity

    # Updates the status of a dish and adjusts the order status accordingly.
    def update_dish_status(self, dish_name, status):
        dish = self.find_dish_by_name(dish_name)
        dish.status = status
        if status == "Pending":
           self.status = "Pending"
        else:  
           self.check_order_status()
  
    # check id status is string and not None.
    def check_valid_status(self, status):
        if status is None:
           raise ValueError("status cannot be None")
        if not isinstance(status, str):
           raise TypeError("status must be a string")
    
    # Returns a list of dishes filtered by status ('Pending', 'Served', or 'all').
    def get_dishes_by_status(self, status):
        self.check_valid_status(status)
        if status not in {"Pending", "Served", "all"}:
           raise ValueError("status must be 'Pending' or 'Served' or 'all'")
        if status == "all":
           return self.dishes[:]
        return [dish for dish in self.dishes if dish.status == status]

    # Calculates and returns the total price of all dishes in the order. 
    def get_total_price(self):
        return sum(dish.get_total_price() for dish in self.dishes) if self.dishes else 0

    # Returns a dictionary representation of the order, including all details.   
    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "table_number": self.table_number,
            "dishes": [dish.to_dict() for dish in self.dishes],
            "status": self.status,
            "total_price": self.get_total_price()
        }
