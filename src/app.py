## app.py
from flask import Flask, request, jsonify
from OrderManager import OrderManager
from Order import Order
from Dish import Dish

# Mapping error types to appropriate HTTP status codes.
ERROR_HTTP_CODES = {
    ValueError: 400,  # Invalid input
    KeyError: 404,  # Missing key (e.g., non-existent order ID)
    LookupError: 404,  # Order or dish not found
    TypeError: 400,  # Incorrect data type
    Exception: 500,  # Unexpected general error
}

# Handles exceptions centrally and returns an appropriate HTTP response code.
def handle_exception(e):
    http_code = ERROR_HTTP_CODES.get(type(e), 500)  # Default to 500
    return jsonify({"error": str(e)}), http_code


app = Flask(__name__)
order_manager = OrderManager()


# Returns the total price of the order at a given table.
@app.route("/orders/<int:table_number>/price", methods=["GET"])
def get_order_price(table_number):
    try:
        price = order_manager.get_order_price(table_number)
        return jsonify({"table_number": table_number, "total_price": price}), 200
    except Exception as e:
        return handle_exception(e)

# Returns the status of the order at a given table.
@app.route("/orders/<int:table_number>/status", methods=["GET"])
def get_order_status(table_number):
    try:
        order_status = order_manager.get_order_status(table_number)
        return jsonify({"table_number": table_number, "status": order_status}), 200
    except Exception as e:
        return handle_exception(e)

# Returns the customer's name associated with the order at a given table.
@app.route("/orders/<int:table_number>/customer_name", methods=["GET"])
def get_customer_name(table_number):
    try:
        customer_name = order_manager.get_customer_name(table_number)
        return jsonify({"table_number": table_number, "customer_name": customer_name}), 200
    except Exception as e:
        return handle_exception(e)

# Updates the customer's name for the order at a given table.
@app.route("/orders/<int:table_number>/change_customer_name/<string:new_name>", methods=["PUT"])
def change_customer_name(table_number, new_name):
    try:
        order_manager.change_customer_name(table_number, new_name)
        return jsonify({"message": "customer name successfully changed"}), 200
    except Exception as e:
        return handle_exception(e)

# Returns the unit price of a specific dish in the order at a given table.
@app.route("/orders/<int:table_number>/dishes/<string:dish_name>/unit_price", methods=["GET"])
def get_dish_unit_price(table_number, dish_name):
    try:
        dish_unit_price = order_manager.get_dish_unit_price(table_number, dish_name)
        return jsonify({"table_number": table_number, "dish_name": dish_name, "unit_price": dish_unit_price}), 200 
    except Exception as e:
        return handle_exception(e)

# Returns the status of a specific dish in the order at a given table.
@app.route("/orders/<int:table_number>/dishes/<string:dish_name>/status", methods=["GET"])
def get_dish_status(table_number, dish_name):
    try:
        dish_status = order_manager.get_dish_status(table_number, dish_name)
        return jsonify({"table_number": table_number, "dish_name": dish_name, "status": dish_status}), 200
    except Exception as e:
        return handle_exception(e)

# Finds and returns order details based on an identifier (e.g., table number, order ID).
@app.route("/order/<string:identifier_type>/<string:identifier_value>", methods=["GET"])
def find_order(identifier_type, identifier_value):
    try:
        order = order_manager.find_order(identifier_type, identifier_value)
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return handle_exception(e)

# Creates a new order and adds it to the system.
@app.route("/add_order", methods=["POST"])
def add_order():
    data = request.get_json()
    customer_name = data.get("customer_name")
    table_number = data.get("table_number")
    try:
        order = Order(customer_name, table_number)
        order_manager.add_order(order)
        return jsonify({"message": "Order successfully added"}), 201
    except Exception as e:
        return handle_exception(e)

# Closes the order at a given table and returns the total order price.
@app.route("/orders/<int:table_number>/close", methods=["PUT"])
def close_order(table_number):
    try:
        total_price = order_manager.close_order(table_number)
        return jsonify({"message": f"Order at table {table_number} closed successfully", "total_price": total_price}), 200
    except Exception as e:
        return handle_exception(e)

# Removes an order based on the given identifier type (e.g., table number or order ID).
@app.route("/remove_order/<string:identifier_type>/<string:identifier_value>", methods=["DELETE"])
def remove_order(identifier_type, identifier_value):
    try:
        order_manager.remove_order(identifier_type, identifier_value)
        return jsonify({"message": "Order successfully removed"}), 200
    except Exception as e:
        return handle_exception(e)

# Adds or removes a dish from an order at a given table.
@app.route("/orders/<int:table_number>/dishes/<string:action>", methods=["PUT"])
def update_dish_in_order(table_number, action):
    data = request.get_json()
    name = data.get("name")
    if action not in ["add", "remove"]:
        return jsonify({"error": "Invalid action. Use 'add' or 'remove'"}), 400

    # Remove dish from order.
    if action == "remove":
        try:
            order_manager.remove_dish_from_order(table_number, name)
            return jsonify({"message": "Dish successfully removed"}), 200
        except Exception as e:
            return handle_exception(e)

    # Add dish to order.
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")
    try:
        dish = Dish(name, quantity, unit_price)
        order_manager.add_dish_to_order(table_number, dish)
        return jsonify({"message": "Dish successfully added"}), 200
    except Exception as e:
        return handle_exception(e)

# Updates the quantity of a specific dish in an order at a given table.
@app.route("/orders/<int:table_number>/dishes/<string:dish_name>/update_quantity/<int:quantity>", methods=["PUT"])
def update_dish_quantity(table_number, dish_name, quantity):
    try:
        order_manager.update_dish_quantity(table_number, dish_name, quantity)
        return jsonify({"message": f"Quantity of '{dish_name}' at table {table_number} updated to {quantity}"}), 200
    except Exception as e:
        return handle_exception(e)

# Updates the status of a specific dish in an order at a given table.
@app.route("/orders/<int:table_number>/dishes/<string:dish_name>/update_status/<string:status>", methods=["PUT"])
def update_dish_status(table_number, dish_name, status):
    try:
        order_manager.update_dish_status(table_number, dish_name, status)
        return jsonify({"message": f"Dish '{dish_name}' status updated to '{status}'"}), 200
    except Exception as e:
        return handle_exception(e)

# Retrieves all table numbers with orders matching the given status.
@app.route("/orders/tables_numbers_by_status/<string:status>", methods=["GET"])
def get_table_numbers_by_order_status(status):
    try:
        tables = order_manager.get_table_numbers_by_order_status(status)
        return jsonify({"status": status, "tables": tables}), 200
    except Exception as e:
        return handle_exception(e)

# Retrieves all dishes in a given order at a table, filtered by their status.
@app.route("/orders/<int:table_number>/dishes_by_status/<string:status>", methods=["GET"])
def get_table_dishes_by_status(table_number, status):
    try:
        dishes = order_manager.get_table_dishes_by_status(table_number, status)
        return jsonify({f"{status.lower()} dishes": [dish.to_dict() for dish in dishes]}), 200
    except Exception as e:
        return handle_exception(e)

# Retrieves all dishes from all orders that match the given status.
@app.route("/dishes_by_status/<string:status>", methods=["GET"])
def get_all_dishes_by_status(status):
    try:
        dishes = order_manager.get_all_dishes_by_status(status)
        return jsonify({"status": status, "dishes": [dish.to_dict() for dish in dishes]}), 200
    except Exception as e:
        return handle_exception(e)

# Calculates the total price of all orders with the given status.
@app.route("/orders/total_price/<string:status>", methods=["GET"])
def get_total_orders_price_by_status(status):
    try:
        total_price = order_manager.total_orders_price_by_status(status)
        return jsonify({"status": status, "total_price": total_price}), 200
    except Exception as e:
        return handle_exception(e)

# Returns the number of created orders.
@app.route("/orders/created_count", methods=["GET"])
def get_created_orders_count():
    return jsonify({"created_orders_count": order_manager.created_orders_num}), 200

# Returns the number of stored (inactive) orders.
@app.route("/orders/stored_count", methods=["GET"])
def get_stored_orders_count():
    return jsonify({"stored_orders_count": order_manager.stored_orders_num}), 200

# Returns the number of currently active orders.
@app.route("/orders/active_count", methods=["GET"])
def get_active_orders_count():
    return jsonify({"active_orders_count": order_manager.active_orders_num}), 200

# Returns a summary of all stored and active orders in the system.
@app.route("/orders/summary", methods=["GET"])
def get_order_manager_summary():
    return jsonify(order_manager.to_dict()), 200