# Python's built-in module for encoding and decoding JSON data
import json
# Python's built-in module for opening and reading URLs
from urllib.request import urlopen

api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
isbn = input("Enter 10 digit ISBN: ").strip()

            # send a request and get a JSON response
resp = urlopen(api + isbn)
            # parse JSON into Python as a dictionary
book_data = json.load(resp)
print(book_data)