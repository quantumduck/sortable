# README

This code was written for the [Sortable coding challenge](https://sortable.com/challenge/). For better compatibility and support, Python 2.7.12 was used. Provided Python 2.7 is installed, the code can be run by cloning the repository into a directory and running `python classify.py` from that directory. The results will be in a file named `results.txt`.

## Files

Other than `classify.py`, the repository contains two files with challenge data: `listings.txt` and `products.txt`. There are also some results from previous runs: `output_*.txt`.

## Approach

I used this challenge as a chance to re-familiarize myself with Python after an absense of a few years. I used an approach based on how I would perform the search manually, rather than trying to research or think up an algorithm. Because the listings included a manufacturer, it made sense classify them using this category first. It is entirely possible for multiple manufacturers to have products with the same model number, but a single manufacturer will have unique names for product lines and models.

## Shortcomings and Improvements

Because the manufacturers list is built first, the 20000 listings are looped through more than once, creating an obvious speed inefficiency. To save on memory, it would also be possible to only load the products file and then go through the listings line by line. I'll give some thoughts to these and other considerations before submitting.
