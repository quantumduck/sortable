import json

listing_file = open('listings.txt', 'r')

all_listings = [json.loads(line) for line in listing_file.readlines()]

print all_listings[0]['title']
