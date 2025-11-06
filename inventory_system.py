"""
Inventory management system for adding, removing, and tracking stock items.
Supports saving to and loading from a JSON file.
"""

import json
from datetime import datetime

stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add a specified quantity of an item to the stock."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        print("Invalid input types for item or quantity.")
        return
    if qty < 0:
        print("Quantity must be non-negative.")
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    log_entry = (
        f"{datetime.now()}: Added {qty} of {item}"
    )
    logs.append(log_entry)


def remove_item(item, qty):
    """Remove a specified quantity of an item from the stock."""
    if not isinstance(item, str) or not isinstance(qty, int):
        print("Invalid input types for item or quantity.")
        return
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Item '{item}' not found in stock.")


def get_qty(item):
    """Return the quantity of the specified item in stock."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError as e:
        print("File not found:", e)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)


def save_data(file="inventory.json"):
    """Save the current inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
    except OSError as e:
        print("Error saving data:", e)


def print_data():
    """Print a report of all items and their quantities."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return a list of items with quantity below the given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Run a sample inventory workflow."""
    logs = []
    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    add_item(123, "ten", logs)  # invalid types
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()
    print("\nLog Entries:")
    for entry in logs:
        print(entry)


if __name__ == "__main__":
    main()
