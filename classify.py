import json
import re

# Punctuation stripping method
def alpha_numeric(string):
    # This method is a bit crude, but it is only necessary for putting product
    # names and model numbers into the same format. This code would need to be
    # modified if any companies have namespaces using non-ASCII characters
    return re.sub(r'[^a-z0-9.]', ' ', string.lower())

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
    num_words = 0
    for index, product in enumerate(all_products):
        # Only look at products made by current manufacturer:
        if product['manufacturer'].lower() == manufacturer:
            # Create a list of key words:
            key_words = alpha_numeric(product['model']).split()
            if 'family' in product:
                key_words += alpha_numeric(product['family']).split()
                # Search for key words in title:
                match = True
                # Split the title into an array of words
                title_words = alpha_numeric(listing['title']).split()
                # Check each word:
                for word in key_words:
                    if word not in title_words:
                        # If a single key word is missing, declare no match:
                        match = False
                    elif title_words.index(word) > 2 * len(key_words):
                        # If the key word is not found near the beginning of
                        # the title, it is likely just an associated product.
                        match = False
                if match:
                    if match_index >= 0:
                        # If there is already a match, print some output:
                        print listing['title']
                        print 'matches both:'
                        print products[match_index]['product_name']
                        print 'and'
                        print products[index]['product_name']
                        if len(key_words) > num_words:
                            print 'Using second match'
                            match_index = index
                            num_words = len(key_words)
                        else:
                            print 'Using first match'
                    match_index = index
                    num_words = len(key_words)
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
            # print match_count

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
