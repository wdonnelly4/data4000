# Campus Store order entry: a Streamlit web app connected to Supabase

import hmac
from datetime import date

import pandas as pd
import streamlit as st

import database as db
from config import get_setting

st.set_page_config(page_title="Campus Store Orders", layout="wide")

# Shows money columns as currency in every table
MONEY = st.column_config.NumberColumn(format="$%.2f")


# ---------- Access control ----------

def check_password():
    """Server-side password gate. Runs before any database access."""
    if st.session_state.get("authenticated"):
        return True

    expected = get_setting("APP_PASSWORD")
    st.title("Campus Store Orders")

    if not expected:
        st.error("This app is locked because APP_PASSWORD has not been configured.")
        return False

    with st.form("login"):
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Enter"):
            # compare_digest compares safely without leaking timing information
            if hmac.compare_digest(password.encode(), str(expected).encode()):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    return False


# ---------- Loading data ----------

def refresh_data():
    """Clear cached tables so the next run pulls fresh data from Supabase."""
    st.cache_data.clear()
    st.session_state.refreshed = True


def load_data():
    """Load customers, products, and orders from Supabase. Stops the app with a message if it fails."""
    try:
        customers = db.get_customers()
        products = db.get_products()
        orders = db.get_orders()
    except Exception:
        st.error("Could not load data from the database. Check the connection settings and try Refresh Data.")
        st.stop()

    # Dictionaries keyed by ID to make lookups simple
    customers = {row["customer_id"]: row for row in customers}
    products = {row["product_id"]: row for row in products}
    return customers, products, orders


# ---------- Display tables ----------

def show_reference_tables(customers, products):
    left, right = st.columns(2)

    with left:
        st.subheader("Customers")
        customer_df = pd.DataFrame(
            [{"Customer ID": cid, "Name": row["name"]} for cid, row in customers.items()]
        )
        st.dataframe(customer_df, hide_index=True, use_container_width=True)

    with right:
        st.subheader("Products")
        product_df = pd.DataFrame([
            {"Product ID": pid, "Product": row["product_name"],
             "Category": row["category"], "Price": float(row["price"])}
            for pid, row in products.items()
        ])
        st.dataframe(product_df, hide_index=True, use_container_width=True,
                     column_config={"Price": MONEY})


def build_order_table(orders, customers, products):
    """Turn order rows into a table with names and a total from the stored unit_price."""
    rows = []
    for order in orders:
        unit_price = float(order["unit_price"])
        rows.append({
            "Order ID": order["order_id"],
            "Customer": customers.get(order["customer_id"], {}).get("name", "Unknown"),
            "Product": products.get(order["product_id"], {}).get("product_name", "Unknown"),
            "Quantity": order["quantity"],
            "Unit Price": unit_price,
            "Total": order["quantity"] * unit_price,
            "Order Date": order["order_date"],
        })
    return pd.DataFrame(rows, columns=["Order ID", "Customer", "Product", "Quantity",
                                       "Unit Price", "Total", "Order Date"])


def show_order_table(df):
    st.dataframe(df, hide_index=True, use_container_width=True,
                 column_config={"Unit Price": MONEY, "Total": MONEY})


# ---------- Order entry ----------

def reset_confirmation():
    """Any change to the order clears the confirmation, so the user must confirm again."""
    st.session_state.confirm = False


def show_order_form(customers, products):
    st.header("New Order")

    customer_id = st.selectbox(
        "Customer", options=list(customers.keys()), index=None,
        placeholder="Choose a customer",
        format_func=lambda cid: f"{customers[cid]['name']} (ID {cid})",
        key="customer_id", on_change=reset_confirmation,
    )
    product_id = st.selectbox(
        "Product", options=list(products.keys()), index=None,
        placeholder="Choose a product",
        format_func=lambda pid: (f"{products[pid]['product_name']} "
                                 f"(${float(products[pid]['price']):.2f})"),
        key="product_id", on_change=reset_confirmation,
    )
    # min_value=1 and step=1 only allow positive whole numbers
    quantity = st.number_input("Quantity", min_value=1, step=1, value=1,
                               key="quantity", on_change=reset_confirmation)

    if customer_id is None or product_id is None:
        st.session_state.reviewed = None
        st.info("Choose a customer and a product to review the order.")
        return

    unit_price = float(products[product_id]["price"])

    # Save exactly what the user is looking at
    st.session_state.reviewed = {
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": int(quantity),
        "unit_price": unit_price,
    }

    st.subheader("Review Order")
    review = pd.DataFrame([{
        "Customer": customers[customer_id]["name"],
        "Product": products[product_id]["product_name"],
        "Quantity": int(quantity),
        "Unit Price": unit_price,
        "Total": int(quantity) * unit_price,
    }])
    st.dataframe(review, hide_index=True, use_container_width=True,
                 column_config={"Unit Price": MONEY, "Total": MONEY})

    st.checkbox("I have reviewed this order and confirm it is correct.", key="confirm")
    st.button("Submit Order", type="primary", on_click=submit_order)


def set_result(level, message, order=None):
    st.session_state.result = {"level": level, "message": message, "order": order}


def submit_order():
    """Runs once per click of Submit Order (a button callback), never on ordinary reruns."""
    reviewed = st.session_state.get("reviewed")

    if not reviewed:
        set_result("error", "Choose a customer and a product before submitting.")
        return
    if not st.session_state.get("confirm"):
        set_result("warning", "Check the confirmation box before submitting. No order was saved.")
        return

    quantity = reviewed["quantity"]
    if not isinstance(quantity, int) or quantity < 1:
        set_result("error", "Quantity must be a positive whole number. No order was saved.")
        return

    # Get the price straight from the database at the moment of submission
    try:
        current_price = db.get_current_price(reviewed["product_id"])
    except Exception:
        set_result("error", "Could not reach the database to check the price. No order was saved.")
        return

    if current_price is None:
        set_result("error", "That product no longer exists. Click Refresh Data. No order was saved.")
        return

    if round(current_price, 2) != round(reviewed["unit_price"], 2):
        st.session_state.confirm = False
        st.cache_data.clear()  # so the review shows the new price
        set_result("warning",
                   f"The price changed from ${reviewed['unit_price']:.2f} to ${current_price:.2f}. "
                   "Review the updated order and confirm again. No order was saved.")
        return

    # Use up the confirmation before inserting
    st.session_state.confirm = False

    order = {
        "customer_id": reviewed["customer_id"],
        "product_id": reviewed["product_id"],
        "quantity": quantity,
        "order_date": date.today().isoformat(),
        "unit_price": current_price,
    }

    try:
        new_order_id = db.insert_order(order)
    except Exception:
        set_result("error", "The order could not be saved because of a database error. No order was saved.")
        return

    if new_order_id is None:
        set_result("error", "The database did not confirm the order. It may not have been saved; "
                            "click Refresh Data and check Order History before trying again.")
        return

    db.get_orders.clear()  # order history must show the new order

    # Verify with a brand-new query
    try:
        saved = db.get_order(new_order_id)
    except Exception:
        saved = None

    if saved is None:
        set_result("warning", f"Order {new_order_id} was saved, but it could not be retrieved "
                              "for verification. Do not submit it again; click Refresh Data.")
    else:
        set_result("success", f"Order {new_order_id} was saved and verified.", saved)


def show_result(customers, products):
    result = st.session_state.get("result")
    if not result:
        return

    getattr(st, result["level"])(result["message"])
    if result["order"]:
        st.subheader("Verification (retrieved from database)")
        show_order_table(build_order_table([result["order"]], customers, products))


# ---------- Order history ----------

def show_order_history(orders, customers, products):
    st.header("Order History")

    # Extra credit: filter by customer
    selected = st.selectbox(
        "Filter by customer", options=[None] + list(customers.keys()),
        format_func=lambda cid: "All customers" if cid is None
        else f"{customers[cid]['name']} (ID {cid})",
        key="history_filter",
    )
    if selected is not None:
        orders = [o for o in orders if o["customer_id"] == selected]

    df = build_order_table(orders, customers, products)
    df = df.sort_values("Order ID", ascending=False)  # newest first

    count_col, value_col = st.columns(2)
    count_col.metric("Orders", len(df))
    value_col.metric("Total value", f"${df['Total'].sum():,.2f}")
    show_order_table(df)


# ---------- Main ----------

def main():
    if not check_password():
        st.stop()

    st.title("Campus Store Orders")
    st.write("Create orders for existing customers. Every order is saved to the Supabase "
             "database and then read back from the database to verify it.")

    st.button("Refresh Data", on_click=refresh_data)
    if st.session_state.pop("refreshed", False):
        st.toast("Data refreshed from Supabase.")

    customers, products, orders = load_data()

    show_reference_tables(customers, products)
    st.divider()
    show_order_form(customers, products)
    show_result(customers, products)
    st.divider()
    show_order_history(orders, customers, products)


main()
