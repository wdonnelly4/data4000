## Define function and parameters
def format_greeting(name, title="Customer"):

## Handling empty name case
    if name.strip() == "":
        return "Hello, Valued Customer!"

    ## Clean up the name
    clean_name = name.strip().title()

    ## Handling whitespace
    first_name = clean_name.split()[0]

    ## Returning final string
    return f"Hello, {first_name} ({title})!"


## Main 
full_name = input("What's your full name? ")
custom_title = input("What title should we use? (Press Enter to skip) ")

# Only override the default title if the user actually typed something
if custom_title.strip() == "":
    greeting = format_greeting(full_name)
else:
    greeting = format_greeting(full_name, custom_title.strip().title())

print(greeting)
