# Use to dowload all Dickens books from the Project Gutenberg Database 
# write them to files in folders "BooksRaw" and "BooksCleaned"

# Be sure to have pg_catalog from Project Gutenberg

import requests
import pandas as pd
import os

catalog = pd.read_csv("pg_catalog.csv")
column_name = "Authors"
list_of_authors = catalog[column_name]
print(list_of_authors)
dickens_books=[]
book_indexes = catalog["Text#"]
book_names=[]
for index, author in enumerate(list_of_authors):
    if type(author)==float:
        continue        
    if "Dickens, Charles" in author and catalog["Language"][index]=="en" and \
    catalog["Type"][index]=="Text":
        in_list=False
        for title in book_names:
            if catalog["Title"][index] in title:
                in_list=True
        if in_list==False:
            book_names.append(catalog["Title"][index])
            dickens_books.append(book_indexes[index])
for books in dickens_books:
    r = requests.get(f'https://gutenberg.org/files/{books}/{books}-0.txt')
    r.encoding = 'utf-8'
    with open(f'BooksRaw/Book{books}.txt', 'w') as f:
        f.write(r.text)

# Check if book file is actually a book

# Iterate through files in the BooksRaw folder, removes if it is html
for bookfile in os.listdir("BooksRaw"):
    # Open each file and check if the first line contains html, if so delete it
    with open("BooksRaw/" + bookfile, "r") as file_text:
        if "html" in file_text.readlines(2)[0]:
            os.remove("BooksRaw/" + bookfile)

# Data Cleaner
# Read lines in raw book text and write to new file in BooksCleaned.
for book in os.listdir("BooksRaw"):
    with open("BooksRaw/" + book, "r") as book_text:
        lines = book_text.readlines()
    for line_number, line in enumerate(lines):
        if "START OF THE PROJECT GUTENBERG EBOOK" in line:
            beginning = line_number + 5
        if "END OF THE PROJECT GUTENBERG EBOOK" in line:
            end = line_number
            break
    with open("BooksCleaned/" + book, "w") as new_book_text:
        for line_number, line in enumerate(lines):
            if line_number in range(beginning, end):
                new_book_text.write(line)
