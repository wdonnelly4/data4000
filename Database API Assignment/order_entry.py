# order_entry.py
# Order entry program: creates a new order for an existing customer,
## saves it to Supabase through the API, then reads it back to verify it.

import os
from datetime import date

from dotenv import load_dotenv
from supabase import create_client

# Column names in the Supabase tables
CUSTOMER_ID_COL = "customer_id"
CUSTOMER_NAME_COL = "name"
PRODUCT_ID_COL = "product_id"
PRODUCT_NAME_COL = "product_name"
PRODUCT_PRICE_COL = "price"
ORDER_ID_COL = "order_id"


# ---------- Connecting and loading data ----------

def connect_to_supabase():
    """Read credentials from .env and return a Supabase client, or None if they're missing."""
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in your .env file.")
        return None

    try:
        return create_client(url, key)
    except Exception:
        print("Error: could not create the Supabase client. Check the values in your .env file.")
        return None


def load_records(client, table_name, id_col):
    """Get every row from a table and return them in a dictionary keyed by ID.
    Returns None if the request fails."""
    try:
        response = client.table(table_name).select("*").order(id_col).execute()
        records = {}
        for row in response.data:
            records[row[id_col]] = row
        return records
    except Exception:
        print(f"Error: could not load the {table_name} table from Supabase.")
        return None


# ---------- Display tables ----------

def show_customers(customers):
    """Print customer ID and name as a table."""
    print("\nCUSTOMERS")
    print(f"{'ID':<6}{'Name':<30}")
    print("-" * 36)
    for customer_id, row in customers.items():
        print(f"{customer_id:<6}{str(row[CUSTOMER_NAME_COL]):<30}")


def show_products(products):
    """Print product ID, name, and price as a table."""
    print("\nPRODUCTS")
    print(f"{'ID':<6}{'Product':<30}{'Price':>10}")
    print("-" * 46)
    for product_id, row in products.items():
        price = float(row[PRODUCT_PRICE_COL])
        print(f"{product_id:<6}{str(row[PRODUCT_NAME_COL]):<30}{price:>10.2f}")


# ---------- Input validation ----------

def get_valid_id(prompt, records, label):
    """Ask for an ID until the user enters a whole number that exists in records."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print(f"'{text}' is not a valid {label} ID. Please enter a whole number from the table.")
            continue

        if value in records:
            return value
        print(f"There is no {label} with ID {value}. Please choose an ID from the table.")


def get_quantity():
    """Ask for a quantity until the user enters a positive whole number."""
    while True:
        text = input("Quantity: ").strip()
        try:
            quantity = int(text)
        except ValueError:
            print(f"'{text}' is not a whole number. Please enter a quantity like 1, 2, or 3.")
            continue

        if quantity > 0:
            return quantity
        print("Quantity must be greater than 0.")


def ask_yes_no(prompt):
    """Ask a Y/N question until the user answers. Returns True for Y, False for N."""
    while True:
        answer = input(prompt).strip().upper()
        if answer == "Y":
            return True
        if answer == "N":
            return False
        print("Please enter Y or N.")


# ---------- Saving and verifying ----------

def save_order(client, order):
    """Insert the order into Supabase. Returns the new order ID, or None if it failed."""
    try:
        response = client.table("orders").insert(order).execute()
    except Exception:
        print("Error: the order could not be saved to the database. Nothing was inserted.")
        return None

    if not response.data:
        print("Error: the database did not confirm the order was saved.")
        return None

    return response.data[0].get(ORDER_ID_COL)


def fetch_order(client, order_id):
    """Run a new query for one order by its ID. Returns the row, or None if not found or failed."""
    try:
        response = client.table("orders").select("*").eq(ORDER_ID_COL, order_id).execute()
    except Exception:
        return None

    if not response.data:
        return None
    return response.data[0]


def show_saved_order(order, customers, products):
    """Print the order retrieved from the database as a table."""
    customer_name = customers[order["customer_id"]][CUSTOMER_NAME_COL]
    product_name = products[order["product_id"]][PRODUCT_NAME_COL]
    unit_price = float(order["unit_price"])
    total = order["quantity"] * unit_price

    print("\nSAVED ORDER (retrieved from database)")
    print(f"{'Order ID':<10}{'Customer':<22}{'Product':<22}{'Qty':>5}"
          f"{'Unit Price':>12}{'Total':>12}  {'Order Date':<12}")
    print("-" * 97)
    print(f"{order[ORDER_ID_COL]:<10}{str(customer_name):<22}{str(product_name):<22}"
          f"{order['quantity']:>5}{unit_price:>12.2f}{total:>12.2f}  {order['order_date']:<12}")


# ---------- One complete order ----------

def place_one_order(client, customers, products):
    """Collect, confirm, save, and verify a single order.
    Every variable here is local, so nothing carries over to the next order."""
    customer_id = get_valid_id("\nCustomer ID: ", customers, "customer")
    product_id = get_valid_id("Product ID: ", products, "product")
    quantity = get_quantity()

    customer_name = customers[customer_id][CUSTOMER_NAME_COL]
    product_name = products[product_id][PRODUCT_NAME_COL]
    unit_price = float(products[product_id][PRODUCT_PRICE_COL]) 
    total = quantity * unit_price

    # Order summary before saving
    print("\nORDER SUMMARY")
    print(f"Customer:   {customer_name}")
    print(f"Product:    {product_name}")
    print(f"Quantity:   {quantity}")
    print(f"Unit price: ${unit_price:.2f}")
    print(f"Total:      ${total:.2f}")

    if not ask_yes_no("Confirm this order? (Y/N): "):
        print("Order cancelled. Nothing was saved.")
        return

    # The database creates order_id
    order = {
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "order_date": date.today().isoformat(),
        "unit_price": unit_price,
    }

    new_order_id = save_order(client, order)
    if new_order_id is None:
        return

    print(f"Success: order {new_order_id} was saved.")

    # Verify with a brand-new query
    saved = fetch_order(client, new_order_id)
    if saved is None:
        print("Verification could not be completed: the saved order was not found in the database.")
    else:
        show_saved_order(saved, customers, products)


# ---------- Main program ----------

def main():
    client = connect_to_supabase()
    if client is None:
        return

    while True:
        # Reload each round so tables and prices are current
        customers = load_records(client, "customers", CUSTOMER_ID_COL)
        products = load_records(client, "products", PRODUCT_ID_COL)
        if not customers or not products:
            print("Cannot continue without customer and product data.")
            return

        show_customers(customers)
        show_products(products)

        place_one_order(client, customers, products)

        # Extra credit: keep going until the user says no
        if not ask_yes_no("\nEnter another order? (Y/N): "):
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
