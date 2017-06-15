import json
# import re # no longer using regular expressions

def alpha_numeric(string):
    # This method is a bit crude, but it is only necessary for putting product
    # names and model numbers into the same format. Some punctuation characters
    # such as slashes and commas may still interfere.
    return string.lower().replace('-', ' ').replace('_', ' ')

def find_manufacturer(listing, manufacturers):
    # Identify the manufacturer in the listing as one of the ones in the list
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
    # This function returns -1 or the index of the product that matches
    # The main logic of the program is here
    match_index = -1 # return value
    num_words = 0 # A crude count of match quality
    for index, product in enumerate(all_products):
        # Only look at products made by current manufacturer:
        if product['manufacturer'].lower() == manufacturer:
            # Create a list of key words:
            key_words = alpha_numeric(product['model']).split()
            if 'family' in product:
                key_words += alpha_numeric(product['family']).split()
            # Split the title into an array of words
            title_words = alpha_numeric(listing['title']).split()
            # Check that each key word appears near the beginning of the listing:
            match = True
            for word in key_words:
                if word not in title_words:
                    # If a single key word is missing, declare no match:
                    match = False
                elif title_words.index(word) > 2 * len(key_words):
                    # If the key word is not found near the beginning of
                    # the title, it is likely just an associated product like
                    # a battery or a case
                    match = False
            if match:
                # A match has occurred, but we do not return the first match
                if match_index >= 0:
                    # If there is already a match, print some output to note
                    # the double match
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
                else:
                    # If a match is not already defined, we use the match we
                    # just found
                    match_index = index
                    num_words = len(key_words)
    return match_index

# Start of program:

# Load all the products into memory:
product_file = open('products.txt', 'r')
all_products = [json.loads(line) for line in product_file.readlines()]
product_file.close()

# Make a list of unique manufacturers:
manufacturers = set([product['manufacturer'].lower()
                    for product in all_products])

# Set up array of objects to store the final results:
matches = [{'product_name': product['product_name'], 'listings': []}
            for product in all_products]
match_count = 0 # variable for console logging to measure progress

# Go through the listings one line at a time:
listing_file = open('listings.txt', 'r')
current_line = listing_file.readline()
while current_line != '':
    # Convert listing to object:
    listing = json.loads(current_line)
    # Determine the manufacturer:
    manufacturer = find_manufacturer(listing, manufacturers)
    if manufacturer:
        # If the manufacturer was found,
        # Go through all the products to check for a match:
        product_index = classify(listing, all_products, manufacturer)
        # If there is a match, put it in the results
        if product_index >= 0:
            # If a match was found, append the listing to the appropriate match
            matches[product_index]['listings'].append(listing)
            match_count += 1
            # print match_count
    # else: # if no manufacturer is found, assume it is not one of our products.
    # Read the next line in the file:
    current_line = listing_file.readline()
# Close the file when all the listings have been checked:
listing_file.close()

# Open a new file for the results:
answer_file = open('results.txt', 'w')
for product in matches:
    # The if statement filters products by whether or not listings were found.
    # To output all products, comment out the line below:
    if len(product['listings']) > 0:
        # Write the result line
        answer_file.write(json.dumps(product) + '\n')
answer_file.close();
