# DATA 4000: Campus Store Orders (Streamlit)

A Streamlit web app for creating orders for existing customers. It reads
customers, products, and orders from Supabase, lets the user build and confirm
an order, saves it through the Supabase API, and then queries the database
again to verify the saved record.

**Live app:** PASTE YOUR STREAMLIT APP LINK HERE

Access is protected by a password. The instructor's access details are provided
privately through the course submission system.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit interface |
| `database.py` | All Supabase API calls |
| `config.py` | Reads credentials from Streamlit secrets or a local `.env` |
| `requirements.txt` | Packages required to run the app |
| `.gitignore` | Keeps `.env` and `.streamlit/secrets.toml` out of GitHub |
| `.env.example` | Example local configuration (placeholders only) |
| `.streamlit/secrets.toml.example` | Example deployment secrets (placeholders only) |

## Setup (local)

1. Create the database by running `DATA_4000_Supabase_Starter.sql` once in
   Supabase > SQL Editor.
2. Install the packages:

       pip install -r requirements.txt

3. Copy `.env.example` to `.env` and fill in your Supabase project URL, your
   **secret** API key, and a password of your choice.
4. Run the app:

       streamlit run app.py

## Deployment (Streamlit Community Cloud)

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create an app from this repository, branch
   `main`, and main file `app.py`.
3. In the app's **Advanced settings > Secrets**, add `SUPABASE_URL`,
   `SUPABASE_KEY`, and `APP_PASSWORD` in the format shown in
   `.streamlit/secrets.toml.example`.
4. Deploy, then test the hosted app.

## How it works

- **Access control:** `check_password()` runs before any database call. The
  password is stored only in deployment secrets and checked on the server with
  `hmac.compare_digest`. Without the password, no data is loaded.
- **Loading data:** `database.py` queries each table through the Supabase API.
  Results are cached with `st.cache_data` so ordinary reruns don't make new API
  calls. **Refresh Data** clears the cache and reloads everything.
- **Order entry:** dropdowns show customer and product names while keeping
  their IDs for the insert. The quantity input only allows whole numbers of 1
  or more.
- **Confirmation:** a review table shows the customer, product, quantity, unit
  price, and total. The user must check the confirmation box before
  submitting. Changing any selection clears the confirmation.
- **No duplicate orders:** the insert runs only inside the Submit Order
  button's `on_click` callback, which Streamlit runs once per click, never on
  ordinary reruns. The confirmation is cleared before the insert, so a second
  click can't save the same order again.
- **Price check:** at submission the app requests the product's current price
  directly from Supabase. If it differs from the reviewed price, nothing is
  saved, the review updates to the new price, and the user must confirm again.
- **Verification:** after the insert, the app takes the generated `order_id`
  from the response and sends a new query for that order. The verification
  table computes the total from the stored `unit_price`. If verification fails,
  the app says the order was saved but could not be retrieved, and does not
  insert again.
- **Order History:** retrieved from Supabase, refreshed after each successful
  order and when Refresh Data is clicked.
- **Extra credit:** the Order History filter shows one customer's orders and
  the total value of those orders from their stored prices.

## Libraries and references

- Streamlit: https://docs.streamlit.io
  - Button callbacks and session state:
    https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
  - Caching: https://docs.streamlit.io/develop/concepts/architecture/caching
  - Secrets management:
    https://docs.streamlit.io/develop/concepts/connections/secrets-management
- Supabase Python client:
  https://supabase.com/docs/reference/python/introduction
- python-dotenv: https://pypi.org/project/python-dotenv/
- pandas (tables): https://pandas.pydata.org/docs/
- `hmac.compare_digest` (password check):
  https://docs.python.org/3/library/hmac.html#hmac.compare_digest

## Testing results (deployed app)

| Test | Expected result | Result |
|---|---|---|
| Open the deployed app | Interface loads after authorized access | Pass |
| View customers and products | Records are retrieved from Supabase | Pass |
| Try an invalid quantity | Input is prevented or rejected | Pass: the field will not accept 0, negatives, or decimals |
| Submit without confirmation | No order is inserted | Pass |
| Confirm and submit a valid order | Exactly one order is inserted | Pass |
| View the verification table | Newly saved order is retrieved from Supabase | Pass |
| Refresh or interact with another widget | Previously submitted order is not inserted again | Pass |
| Refresh order history | Saved order remains visible | Pass |
| Extra credit: filter order history | Only that customer's orders and their total are shown | Pass |

## Screenshots

### Order entry interface
ADD SCREENSHOT HERE

### Successfully verified order
ADD SCREENSHOT HERE
