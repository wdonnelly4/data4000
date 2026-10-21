## Inventory Reorder Analyzer with API Spot Check
import requests


def get_on_hand():
    """Ask for the on-hand quantity until the user enters a whole number of 0 or more."""
    while True:
        try:
            on_hand = int(input("On hand: "))
            if on_hand >= 0:
                return on_hand
            print("On-hand quantity can't be negative. Try again.")
        except ValueError:
            print("On-hand quantity must be a whole number. Try again.")


def get_threshold(seed):
    """Pick the reorder threshold from the seed."""
    if seed % 3 == 0:
        return 15
    elif seed % 3 == 1:
        return 12
    else:
        return 9


def spot_check(term):
    """Call the iTunes Search API. Returns (songs_returned, api_status)."""
    url = "https://itunes.apple.com/search"
    params = {"entity": "song", "limit": 5, "term": term}

    ## Anything that goes wrong here is a FAILED call
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return "N/A", "FAILED"

    ## Anything missing or the wrong shape is an INVALID_RESPONSE
    try:
        data = response.json()
        results = data["results"]
        song_count = 0
        for item in results:
            if item.get("kind") == "song":
                song_count += 1
        return song_count, "OK"
    except (ValueError, KeyError, TypeError, AttributeError):
        return "N/A", "INVALID_RESPONSE"


def main():
    ## Student key and seed
    student_key = input("Student key: ")
    seed = sum(ord(ch) for ch in student_key.strip())

    ## Threshold from the seed
    threshold = get_threshold(seed)

    total_skus = 0
    reorder_count = 0

    ## SKU entry loop
    while True:
        sku = input("SKU: ").strip()

        if sku.upper() == "DONE":
            break
        if sku == "":
            print("SKU can't be blank. Try again.")
            continue

        on_hand = get_on_hand()
        total_skus += 1

        ## Reorder decision
        if on_hand < threshold:
            reorder_count += 1
            print(f"{sku}: REORDER")
        else:
            print(f"{sku}: OK")

    ## Pick the search term from the seed
    term = "weezer" if seed % 2 == 0 else "drake"

    ## API request and JSON processing
    songs_returned, api_status = spot_check(term)

    ## Results
    print(f"Seed: {seed}")
    print(f"Threshold: {threshold}")
    print(f"SKUs entered: {total_skus}")
    print(f"Reorder flagged: {reorder_count}")
    print(f"Spotcheck term: {term}")
    print(f"Songs returned: {songs_returned}")
    print(f"API status: {api_status}")


if __name__ == "__main__":
    main()