## Point-of-Sale Checkout System

def get_item_name():
    """Ask for an item name. Returns the cleaned name, or None if the cashier typed DONE."""
    while True:
        name = input("Item name (or DONE to finish): ").strip()
        if name.upper() == "DONE":
            return None
        if name == "":
            print("Item name can't be empty. Try again.")
        else:
            return name


def get_unit_price():
    """Ask for a unit price until the user enters a float greater than 0."""
    while True:
        try:
            price = float(input("Unit price: "))
            if price > 0:
                return price
            print("Price must be greater than 0. Try again.")
        except ValueError:
            print("That's not a valid number. Try again.")


def get_quantity():
    """Ask for a quantity until the user enters a whole number of at least 1."""
    while True:
        try:
            quantity = int(input("Quantity: "))
            if quantity >= 1:
                return quantity
            print("Quantity must be at least 1. Try again.")
        except ValueError:
            print("Quantity must be a whole number. Try again.")


def main():
    ## Student key and seed
    student_key = input("Student key: ")
    seed = sum(ord(ch) for ch in student_key.strip())

    ## Running totals start at zero
    subtotal = 0.0
    units = 0

    ## Item entry loop with validation
    while True:
        name = get_item_name()
        if name is None:
            break  ## cashier typed DONE

        price = get_unit_price()
        quantity = get_quantity()

        subtotal += price * quantity
        units += quantity
        print(f"Added {quantity} x {name} at ${price:.2f}")

    ## Discount logic
    if units >= 10 or subtotal >= 100:
        discount_percent = 10
    else:
        discount_percent = 0

    total = subtotal * (1 - discount_percent / 100)

    ## Seed based member perk
    if seed % 2 == 1:
        perk_applied = "YES"
        total -= 3.00
    else:
        perk_applied = "NO"

    ## Total can never go below $0.00
    if total < 0:
        total = 0.0

    ## Results
    print(f"Seed: {seed}")
    print(f"Units: {units}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: {discount_percent}%")
    print(f"Perk applied: {perk_applied}")
    print(f"Total: ${total:.2f}")


if __name__ == "__main__":
    main()


try:
    price = float(input("Unit price: "))
except ValueError:
    print("That's not a valid number. Try again.")