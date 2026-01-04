## Dish.py
## Represents a dish in an order, including its name, quantity, unit_price, and status.

class Dish:
    # constructor
    # Dish status must be 'Pending' or 'Served'.
    def __init__(self, name, quantity, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.status = "Pending" # in the beginning.

    @property
    def name(self):
        return self.__name

    # check if name is str type, not empty and not None
    @name.setter
    def name(self, name):
        if name is None:
           raise ValueError("name cannot be None")
        if not isinstance(name, str):
           raise TypeError("name must be a string")
        name = name.strip()  
        if not name:
           raise ValueError("name cannot be empty")
        self.__name = name

    @property
    def quantity(self):
        return self.__quantity

    # check if quantity is int type, not unpositive and not None
    @quantity.setter
    def quantity(self, quantity):
        if quantity is None:
           raise ValueError("quantity cannot be None")
        if not isinstance(quantity, int):
           raise TypeError("quantity must be a integer")
        if quantity <= 0:
           raise ValueError("quantity must be positive")
        self.__quantity = quantity

    @property
    def unit_price(self):
        return self.__unit_price

    # check if unit_price is number type, not unpositive and not None
    @unit_price.setter
    def unit_price(self, unit_price):
        if unit_price is None:
           raise ValueError("unit price cannot be None")
        if not isinstance(unit_price, (int, float)):
           raise TypeError("unit price must be a number")
        if unit_price <= 0:
           raise ValueError("unit price must be positive")
        self.__unit_price = float(unit_price)
  
    @property
    def status(self):
        return self.__status

    # dish status can be or 'Pending' or 'Served'.
    @status.setter
    def status(self, status):
        if status is None:
           raise ValueError("status cannot be None")
        if not isinstance(status, str):
           raise TypeError("status must be a string")
        if status not in {"Pending", "Served"}:
           raise ValueError("status must be 'Pending' or 'Served'")
        self.__status = status

    # total price of dish
    def get_total_price(self):
        return self.quantity * self.unit_price
      
    def to_dict(self):
        return {
            "name": self.name,
            "unit price": self.unit_price,
            "quantity": self.quantity,
            "status": self.status,
            "total price": self.get_total_price()
        }
