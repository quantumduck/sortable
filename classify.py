import json
import re

# Punctuation stripping method
def alpha_numeric(string):
    # This method is a bit crude, but it is only necessary for putting product
    # names and model numbers into the same format. This code would need to be
    # modified if any companies have namespaces using non-ASCII characters
    return re.sub(r'[^a-z0-9]', ' ', string.lower())

def find_manufacturer(listing, manufacturers):
    # Find the manufacturer from the given list
    manufacturer = False
    for man in manufacturers:
        if listing['manufacturer'].lower().find(man) >= 0:
            if manufacturer:
                # Do not allow manufacturer to be defined twice:
                raise ValueError(listing['manufacturer'] + ' matched both ' +
                                  manufacturer + ' and ' + man)
            manufacturer = man
    return manufacturer

def classify(listing, products, manufacturer):
    # This function returns False or the index of the product that matches
    match_index = -1
    for index, product in enumerate(all_products):
        # Only look at products made by current manufacturer:
        if product['manufacturer'].lower() == manufacturer:
            # Create a list of key words:
            key_words = alpha_numeric(product['model']).split()
            if 'family' in product:
                key_words += alpha_numeric(product['family']).split()
                # Search for key words in title:
                match = True
                for word in key_words:
                    if alpha_numeric(listing['title']).find(word) < 0:
                        # If a single key word is missing, declare no match:
                        match = False
                if match:
                    if match_index >= 0:
                        print match_index
                        print index
                        raise ValueError(listing['title'] +
                                    ' matched more than one product:')
                    match_index = index
    return match_index

# Load all the products into memory:
product_file = open('products.txt', 'r')
all_products = [json.loads(line) for line in product_file.readlines()]
product_file.close()

# Divide by manufacturers first:
manufacturers = set([product['manufacturer'].lower()
                    for product in all_products])

# Set up array for the final results:
matches = [{'product_name': product['product_name'], 'listings': []}
            for product in all_products]
match_count = 0

# Go through the listings line by line:
listing_file = open('listings.txt', 'r')
current_line = listing_file.readline()
while current_line != '':
    # Convert listing to object:
    listing = json.loads(current_line)
    # Determine the manufacturer:
    manufacturer = find_manufacturer(listing, manufacturers)
    if manufacturer:
        # Go through all the products to check for a match:
        product_index = classify(listing, all_products, manufacturer)
        # If there is a match, put it in the results
        if product_index >= 0:
            matches[product_index]['listings'].append(listing)
            match_count += 1
            print match_count

    # Read the next line in the file:
    current_line = listing_file.readline()

# Close the file when all the listings have been checked:
listing_file.close()

answer_file = open('results.txt', 'w')
for product in matches:
    # Only print out the products that were found:
    if len(product['listings']) > 0:
        answer_file.write(json.dumps(product) + '\n')
answer_file.close();
