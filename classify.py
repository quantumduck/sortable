import json

# Load both the text files:

listing_file = open('listings.txt', 'r')
all_listings = [json.loads(line) for line in listing_file.readlines()]
listing_file.close()

product_file = open('products.txt', 'r')
all_products = [json.loads(line) for line in product_file.readlines()]
product_file.close()

# Divide by manufacturers first:

manufacturers = [{'name': manufacturer, 'listings': []} for manufacturer in
    set([product['manufacturer'] for product in all_products])]

for manufacturer in manufacturers:
    for listing in all_listings:
        if listing['manufacturer'].find(manufacturer['name']) >= 0:
            manufacturer['listings'].append(listing)

print manufacturers[8]['name']
print manufacturers[8]['listings']
