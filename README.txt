# Examining Dickens’ Thoughts About Various Professions Based on Linguistic Analysis:

This repository is an exploratory project that used the Project Gutenberg database and NLP libraries to find the adjectives that author's (specifically Dickens' in this case) use to describe professions (or any keyword of your choice). We also applied sentiment analysis to these adjectives to get a sense of Dickens' opinions on them.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libaries/packages:

Wordcloud visualization tool
```bash
pip install matplotlib
pip install pandas
pip install wordcloud

```
spaCy NLP
```bash
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```
NLTK Library
```bash
pip install --user -U nltk
```


## Usage

Collecting Data:
Running the code cells in Datascrapper.ipynb will populate the folders BooksRaw and BooksCleaned with pure text files of the books and cleaned versions respectfully. 

If you would prefer to  examine the works of any author contained in the Project Gutenberg database this can be easily done. The only change required to get data from a different is to replace "Dickens, Charles" in the following line of code (in the second code block of the notebook) with your preferred author. 
```bash
if "Dickens, Charles" in author and catalog["Language"][index]=="en" and \
```
Additionally, if significant time has passed since March 2022 it would be worthwhile to replace pg_catalog.csv with the newest catalog from the Project Gutenberg website. 

text_analysis.py contains all of the data processing of this project. The two functions that would be most useful to interface with are: 
find_adj_all_words_all_books(wordbank): Given a list of lists of keywords (with the main list being of different types of words, and the sub lists being synonyms) returns a list of all the adjectives found in all the books for each keyword. The results are written into a text file which can then be used for data visualization. 

sentiment_countifier_individual(adjectives):
given a list of adjectives it will return the average sentiment score (which is split into a positive, neutral, and negative score).

Visualization.py contains the code we used for visualization and the following
function are useful for visualization:



Running the code with a different wordbank:

Change the wordbank to whatever set of keywords you desire. Then delete
all_adjectives_expanded.txt. Now, if you run text_analysis.py (or run the 
computational essay) a list of adjectives based on your new word bank will be
generate in a new all_adjectives_expanded.txt file in the Outputs folder. 
Warning: this function will take a very long time with any sizable wordbank. For
example, a single word will usually take around couple of minutes, depending on how
many times it is used in the books. 



```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.