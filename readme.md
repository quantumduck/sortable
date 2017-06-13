# README

This code was written for the [Sortable coding challenge](https://sortable.com/challenge/). For better compatibility and support, Python 2.7.12 was used. Provided Python 2.7 is installed, the code can be run by cloning the repository into a directory and running `python classify.py` from that directory. The results will be in a file named `results.txt`.

## Files

Other than `classify.py`, the repository contains two files with challenge data: `listings.txt` and `products.txt`. There are also some results from previous runs saved as: `output_*.txt`.

## Approach

I used this challenge as a chance to re-familiarize myself with Python after an absense of a few years. I used an approach based on how I would perform the search manually, rather than trying to research or think up an algorithm. Because the listings included a manufacturer, it made sense classify them using this category first. It is entirely possible for multiple manufacturers to have products with the same model number, but a single manufacturer will have unique names for product lines and models.

After refactoring to reduce the memory footprint, and increasing the speed, I realized there were a lot of double and false matches occuring. By logging the double matches, I was able to realize that some items were matched more than once because there were listings for product accessories, while others were listed more than once because one product contained all the key words of another. To avoid this, I added logic to disallow matches if the key words were not at the start of the title. The buffer was twice the number of key words.

I also realized that dots were significant and added those back into the list of non-replaced characters. I then went back to the old behaviour of only replacing hyphens and underscores, since the false positives as a result of stripping punctuation were a worse problem than the false negatives caused by punctuation next to the key words.

## Shortcomings and Improvements

There has also been no optimizaton done for the quality of the matching. The rule of checking for the n key words in the first 2n words of the title has no present justification unless the data gets reviewed more carefully.

Some products in the list cannot be differentiated. In one case, the product has different names in different locales; in another case, the product is listed twice, but one of the product names uses a hyphen instead of an underscore. At this time, all the listings associated with such a product will be associated with the first one in the product list, while the second gets no listings.
