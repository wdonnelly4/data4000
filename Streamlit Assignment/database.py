# database.py
# All Supabase API calls for the app live here.
# Functions raise an exception if a request fails; app.py catches it and shows a friendly message.

import streamlit as st
from supabase import create_client

from config import get_setting


@st.cache_resource
def get_client():
    """Create the Supabase client once and reuse it on every rerun."""
    url = get_setting("SUPABASE_URL")
    key = get_setting("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Supabase credentials are not configured.")
    return create_client(url, key)


# The cached functions below keep data between reruns so every click
# doesn't trigger new API calls. The Refresh Data button clears this cache.

@st.cache_data(show_spinner=False)
def get_customers():
    response = (get_client().table("customers")
                .select("customer_id, name")
                .order("customer_id")
                .execute())
    return response.data


@st.cache_data(show_spinner=False)
def get_products():
    response = (get_client().table("products")
                .select("product_id, product_name, category, price")
                .order("product_id")
                .execute())
    return response.data


@st.cache_data(show_spinner=False)
def get_orders():
    response = (get_client().table("orders")
                .select("*")
                .order("order_id")
                .execute())
    return response.data


# The functions below are never cached: they must always ask the database directly.

def get_current_price(product_id):
    """Return the product's current price straight from the database, or None if it no longer exists."""
    response = (get_client().table("products")
                .select("price")
                .eq("product_id", product_id)
                .execute())
    if not response.data:
        return None
    return float(response.data[0]["price"])


def insert_order(order):
    """Insert one order and return the order_id the database generated (None if not confirmed)."""
    response = get_client().table("orders").insert(order).execute()
    if not response.data:
        return None
    return response.data[0].get("order_id")


def get_order(order_id):
    """Run a new query for one order by ID. Returns the row, or None if it isn't found."""
    response = (get_client().table("orders")
                .select("*")
                .eq("order_id", order_id)
                .execute())
    if not response.data:
        return None
    return response.data[0]
