# DATA4000 Assignment 5

Two terminal programs that handle invalid user input without crashing.

## Installation

    pip install requests

## How to run

From the project folder in the terminal:

    python3 pos_checkout.py
    python3 inventory_spotcheck.py

## Exercise 1: Point-of-Sale Checkout (pos_checkout.py)

Cashier enters items (name, unit price, quantity) until typing DONE.
Invalid prices and quantities are rejected and reprompted. Also, applies a 10%
discount for 10+ units or a $100+ subtotal, plus a $3.00 member perk when
the seed is odd.

### Example run

- Example run for pos_checkout.py: 

"pos_checkout.py"
Student key: willem
Item name (or DONE to finish): Shirt
Unit price: abc
That's not a valid number. Try again.
Unit price: -5
Price must be greater than 0. Try again.
Unit price: 20
Quantity: 0
Quantity must be at least 1. Try again.
Quantity: 3
Added 3 x Shirt at $20.00
Item name (or DONE to finish): 
Item name can't be empty. Try again.
Item name (or DONE to finish): Hat
Unit price: 15
Quantity: 2
Added 2 x Hat at $15.00
Item name (or DONE to finish): Water Bottle
Unit price: 12
Quantity: 1
Added 1 x Water Bottle at $12.00
Item name (or DONE to finish): DONE
Seed: 650
Units: 6
Subtotal: $102.00
Discount: 10%
Perk applied: NO
Total: $91.80

## Exercise 2: Inventory Spot Check (inventory_spotcheck.py)

Staff enter SKUs and on hand counts until typing DONE. Items below the
seed-based threshold are flagged for reorder. The program then calls the
iTunes Search API and reports how many songs came back.

### Example run

- Example run for inventory_spotcheck.py

"inventory_spotcheck.py"
Student key: willem
SKU: A100
On hand: ten
On-hand quantity must be a whole number. Try again.
On hand: -1
On-hand quantity can't be negative. Try again.
On hand: 5
A100: REORDER
SKU: 
SKU can't be blank. Try again.
SKU: B200
On hand: 50
B200: OK
SKU: C300
On hand: 9
C300: OK
SKU: DONE
Seed: 650
Threshold: 9
SKUs entered: 3
Reorder flagged: 1
Spotcheck term: weezer
Songs returned: 5
API status: OK