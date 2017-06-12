import json
import re

# Load both the text files:

listing_file = open('listings.txt', 'r')
all_listings = [json.loads(line) for line in listing_file.readlines()]
listing_file.close()

product_file = open('products.txt', 'r')
all_products = [json.loads(line) for line in product_file.readlines()]
product_file.close()

def alpha_numeric(string):
    return re.sub(r'[^a-z0-9]', ' ', string.lower())

# Divide by manufacturers first:
manufacturers = [
    {'name': manufacturer.lower(), 'listings': []}
    for manufacturer in set([product['manufacturer']
    for product in all_products])]
# Add a catch_all for the listings that don't match:
manufacturers.append({'name': 'other', 'listings': []})

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
match_count = 0

# Loop over all the products:
for product in all_products:
    matches.append({'product_name': product['product_name'], 'listings': []})
    # Make a list of the basic info we have
    key_words = alpha_numeric(product['model']).split()
    if 'family' in product:
        key_words += alpha_numeric(product['family']).split()

    # Loop over only the listings relevant to that particular manufacturer:
    manufacturer = filter(
        lambda man: man['name'] == product['manufacturer'].lower(),
        manufacturers)[0]

    for listing in manufacturer['listings']:
        match = True
        for word in key_words:
            if alpha_numeric(listing['title']).find(word) < 0:
                match = False
        if match:
            matches[-1]['listings'].append(listing)
            match_count += 1
            print match_count

final_answer = open('output.txt', 'w')
for product in matches:
    if len(product['listings']) > 0:
        final_answer.write(json.dumps(product) + '\n')
final_answer.close();
