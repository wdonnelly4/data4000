# DATA 4000: Campus Store Order Entry

A terminal program that creates new orders for existing customers. It loads
customers and products from Supabase, validates every input, shows an order
summary for confirmation, saves the order through the Supabase API, and then
queries the database again to verify the saved record.

## Files

| File | Purpose |
|---|---|
| `order_entry.py` | The order entry program |
| `requirements.txt` | Python packages to install |
| `.env.example` | Template for credentials (placeholders only) |
| `.gitignore` | Keeps `.env` and other local files out of GitHub |

## Setup

1. Create the database by running `DATA_4000_Supabase_Starter.sql` once in
   Supabase > SQL Editor > New query. The final check should show
   20 customers, 12 products, and 60 orders.
2. Install the packages:

       pip install -r requirements.txt

3. Copy `.env.example` to a new file named `.env` and fill in your own values
   from Supabase > Project Settings > API:
   - `SUPABASE_URL`: your project URL
   - `SUPABASE_KEY`: your **secret** (service_role) key. The tables have row
     level security with no public access, so the public/anon key will not work.

   `.env` is listed in `.gitignore` and is never committed.

## How to run

    python order_entry.py

The program shows the customer and product tables, then asks for a customer
ID, product ID, and quantity. After you confirm with Y, it saves the order and
prints the record retrieved from the database. You can then enter another order
or exit.

## How it works

- **Loading data:** `load_records()` queries each table with
  `select("*")` and stores the rows in a dictionary keyed by ID, so checking
  whether an ID exists is a simple `in` test.
- **Validation:** `get_valid_id()` and `get_quantity()` loop until the input is
  valid. `try/except ValueError` catches text and decimals; `if` checks catch
  unknown IDs, zero, and negative numbers.
- **Saving:** `save_order()` inserts the order with the price taken from the
  database and today's date. The database generates `order_id`. A success
  message prints only after the insert response confirms the new row.
- **Verifying:** `fetch_order()` sends a new query filtered with
  `.eq("order_id", new_id)`. The total in the verification table is calculated
  from the stored `unit_price`. If the query fails, the program reports that
  verification could not be completed and does not insert again.
- **Extra credit:** after each order or cancellation the program asks whether
  to enter another. All order details live inside `place_one_order()`, so
  nothing carries over between orders.

## Libraries and references

- `supabase` (Supabase Python client):
  https://supabase.com/docs/reference/python/introduction
- `python-dotenv` (loads credentials from `.env`):
  https://pypi.org/project/python-dotenv/

## Testing results

| Test | Input | Expected | Result |
|---|---|---|---|
| Text instead of a customer ID | `hello` | Helpful message; asks again | Pass |
| Customer ID that does not exist | `99` | Rejects the ID; asks again | Pass |
| Product ID that does not exist | `999` | Rejects the ID; asks again | Pass |
| Quantity 0, -2, 1.5, hello | `0`, `-2`, `1.5`, `hello` | Rejects each value; asks again | Pass |
| Cancel at the confirmation prompt | `N` | No order is inserted | Pass |
| Confirm a valid order | `Y` | Exactly one order is inserted | Pass |
| Retrieve the newly created order | (automatic) | Saved order appears in the verification table | Pass |
| Enter another order (extra credit) | `Y` then `N` | Starts a fresh order, then exits | Pass |

## Example run

```
python3 order_entry.py

CUSTOMERS
ID    Name                          
------------------------------------
1     Avery Morgan                  
2     Jordan Patel                  
3     Taylor Chen                   
4     Casey Rivera                  
5     Riley Brooks                  
6     Morgan Lee                    
7     Jamie Wilson                  
8     Alex Kim                      
9     Cameron Davis                 
10    Quinn Garcia                  
11    Sam Parker                    
12    Drew Johnson                  
13    Skyler Reed                   
14    Reese Martin                  
15    Rowan Lewis                   
16    Peyton Clark                  
17    Finley Hall                   
18    Emerson Young                 
19    Dakota Allen                  
20    Harper Scott                  

PRODUCTS
ID    Product                            Price
----------------------------------------------
1     Notebook                            4.50
2     Pen Set                             6.00
3     Backpack                           45.00
4     Water Bottle                       18.00
5     Hoodie                             39.00
6     T-Shirt                            19.00
7     USB Drive                          12.50
8     Wireless Mouse                     24.00
9     Desk Lamp                          29.00
10    Coffee Mug                         10.00
11    Planner                            15.00
12    Laptop Stand                       35.00

Customer ID: hello
'hello' is not a valid customer ID. Please enter a whole number from the table.

Customer ID: 99
There is no customer with ID 99. Please choose an ID from the table.

Customer ID: 1
Product ID: 999
There is no product with ID 999. Please choose an ID from the table.
Product ID: 5
Quantity: 0
Quantity must be greater than 0.
Quantity: -2
Quantity must be greater than 0.
Quantity: 1.5
'1.5' is not a whole number. Please enter a quantity like 1, 2, or 3.
Quantity: hello
'hello' is not a whole number. Please enter a quantity like 1, 2, or 3.
Quantity: 2

ORDER SUMMARY
Customer:   Avery Morgan
Product:    Hoodie
Quantity:   2
Unit price: $39.00
Total:      $78.00
Confirm this order? (Y/N): maybe
Please enter Y or N.
Confirm this order? (Y/N): N
Order cancelled. Nothing was saved.

Enter another order? (Y/N): Y

CUSTOMERS
ID    Name                          
------------------------------------
1     Avery Morgan                  
2     Jordan Patel                  
3     Taylor Chen                   
4     Casey Rivera                  
5     Riley Brooks                  
6     Morgan Lee                    
7     Jamie Wilson                  
8     Alex Kim                      
9     Cameron Davis                 
10    Quinn Garcia                  
11    Sam Parker                    
12    Drew Johnson                  
13    Skyler Reed                   
14    Reese Martin                  
15    Rowan Lewis                   
16    Peyton Clark                  
17    Finley Hall                   
18    Emerson Young                 
19    Dakota Allen                  
20    Harper Scott                  

PRODUCTS
ID    Product                            Price
----------------------------------------------
1     Notebook                            4.50
2     Pen Set                             6.00
3     Backpack                           45.00
4     Water Bottle                       18.00
5     Hoodie                             39.00
6     T-Shirt                            19.00
7     USB Drive                          12.50
8     Wireless Mouse                     24.00
9     Desk Lamp                          29.00
10    Coffee Mug                         10.00
11    Planner                            15.00
12    Laptop Stand                       35.00

Customer ID: 1,5,2
'1,5,2' is not a valid customer ID. Please enter a whole number from the table.

Customer ID: 1
Product ID: 5
Quantity: 2

ORDER SUMMARY
Customer:   Avery Morgan
Product:    Hoodie
Quantity:   2
Unit price: $39.00
Total:      $78.00
Confirm this order? (Y/N): Y
Success: order 1000 was saved.

SAVED ORDER (retrieved from database)
Order ID  Customer              Product                 Qty  Unit Price       Total  Order Date  
-------------------------------------------------------------------------------------------------
1000      Avery Morgan          Hoodie                    2       39.00       78.00  2026-11-03  

Enter another order? (Y/N): N
Goodbye.
```
