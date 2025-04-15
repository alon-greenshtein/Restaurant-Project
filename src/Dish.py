## Dish.py
## Represents a dish in an order, including its name, quantity, price, and status.

class Dish:
    # constructor
    # Dish status must be 'Pending' or 'Served'.
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
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
    def price(self):
        return self.__price

    # check if price is number type, not unpositive and not None
    @price.setter
    def price(self, price):
        if price is None:
           raise ValueError("price cannot be None")
        if not isinstance(price, (int, float)):
           raise TypeError("price must be a number")
        if price <= 0:
           raise ValueError("price must be positive")
        self.__price = float(price)
  
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
        return self.quantity * self.price
      
    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.get_total_price(),
            "status": self.status
        }
