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

manufacturers.append({'name': 'unknown', 'listings': [], 'products': []})

for listing in all_listings:
    not_found = True
    for manufacturer in manufacturers:
        if listing['manufacturer'].lower().find(manufacturer['name']) >= 0:
            manufacturer['listings'].append(listing)
            not_found = False
    if not_found:
        manufacturers[-1]['listings'].append(listing)

print [m['name'] for m in manufacturers]
