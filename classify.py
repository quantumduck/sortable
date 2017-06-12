import json

# Load both the text files:

listing_file = open('listings.txt', 'r')
all_listings = [json.loads(line) for line in listing_file.readlines()]
listing_file.close()

product_file = open('products.txt', 'r')
all_products = [json.loads(line) for line in product_file.readlines()]
product_file.close()

# Divide by manufacturers first:
manufacturers = [
    {'name': manufacturer.lower(), 'listings': []}
    for manufacturer in set([product['manufacturer']
    for product in all_products])]

# Add a catch_all for the listings that don't match:
manufacturers.append({'name': 'unknown', 'listings': []})

# Populate the manufacturers array with matching listings:
for listing in all_listings:
    not_found = True
    for manufacturer in manufacturers:
        if listing['manufacturer'].lower().find(manufacturer['name']) >= 0:
            manufacturer['listings'].append(listing)
            not_found = False
    if not_found:
        manufacturers[-1]['listings'].append(listing)

# Set up array for the final results:
matches = []

# Loop over all the products:
for product in all_products:
    matches.append({'product_name': product['product_name'], 'listings': []})
    # Make a list of the basic info we have
    key_words = product['model'].lower().split()
    if 'family' in product:
        key_words += product['family'].lower().split()

    # Loop over only the listings relevant to that particular manufacturer:
    manufacturer = filter(
        lambda man: man['name'] == product['manufacturer'].lower(),
        manufacturers)[0]

    for listing in manufacturer['listings']:
        match_count = 0
        for word in key_words:
            match_count += listing['title'].lower().split().count('word')
            print listing['title'].lower().split()
            print word
        if match_count > 0:
            print product['product_name']
            print listing['title']
