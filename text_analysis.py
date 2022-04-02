"""
Functions to read and break up all text and identify occurances of keyword
and their adjectives.
"""

import os
import nltk
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

from professions import word_bank

def find_occurances_of_keyword(keyword, text):
    """
    Finds occurrences of the selected keyword within the text provided
    then return a list of indexed occurrences of the word within the text.

    Args:
        keyword: A string which represents the selected keyword.
        text: A tokenized text given as a list of strings of words and
        punctuation.
    Returns:
        Returns a list of indexes (integers) for each occurance
        of the keyword.
    """
    list_of_indexes = []
    for index, word in enumerate(text):
        if keyword == word:
            list_of_indexes.append(index)
    return list_of_indexes


def find_sentences_with_keyword(keyword, text):
    """
    Find the sentence that contextualizes the occurence of a keyword and return
    a list of indices that represent the range of each sentence containing the
    keyword. Calls on find_occurances_of_keywords to find all of the sentences.
    This method determines the start and end of sentences by interating through
    the characters in the string until it hits end punctuation.
    Args:
        keyword: A string representing a word to contextualize in a sentence.
        text: A tokenized text given as a list of strings of words and
        punctuation.

    Returns:
        A list of strings that are sentences containing the keyword.
    """
    keyword_locations = find_occurances_of_keyword(keyword, text)
    end_punctuation = [".", "!", "?"]
    sentence_ranges = []
    for i in keyword_locations:
        next_word = i + 1
        while text[next_word] not in end_punctuation:
            next_word += 1
        end_location = next_word + 1
        previous_word = i-1
        while text[previous_word] not in end_punctuation:
            previous_word -= 1
        start_location = previous_word + 1
        if (start_location, end_location) not in sentence_ranges:
            sentence_ranges.append((start_location, end_location))
    sentences = []
    for range_ in sentence_ranges:
        new_sentence = TreebankWordDetokenizer().detokenize(
            (text[range_[0]:range_[1]]))
        sentences.append(new_sentence.replace(" ’ ", "’"))
    return sentences


def look_for_adjectives(keyword, sentence):
    """
    This function parses through a provided sentence and identifies
    adjectives that are connected with the keyword. It does this by following
    the tree of every token in the sentence until they hit the root of the
    sentence. If the word is both an ajective and the keyword was on its path
    to the root then the adjective is added to the list.

    Args:
        keyword: A string representing the target keyword to be described.
        sentence: A string consisting of the provided sentence.

    Returns:
        A list of strings representing adjectives that are used in
        correlation with the keyword in the given sentence.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    adjectives = []
    for token in doc:
        working_token = token
        while working_token.dep_ != "ROOT":
            if working_token.head.text == keyword and (token.pos_ == ("ADJ")):
                adjectives.append(token.text)
                break
            if working_token.head.text == working_token.text:
                break
            working_token = working_token.head
    return adjectives


def find_adj_in_all_sentences(keyword, path):
    """
    The function opens a file of text, tokenizes the text, finsd all instances
    of the keyword and its context, and then runs look_for_adjectives on each
    of these sentences to get a complete list of adjectives.

    Args:
        keyword: String of a keyword that is being examined
        path: A string that represents a path to a book
    Returns
        A list of adjectives in the book which are connected to the
        keyword.
    """
    with open(path) as book:
        contents = book.read()
        text = nltk.word_tokenize(contents)
    adj = []
    for item in find_sentences_with_keyword(keyword, text):
        adj += look_for_adjectives(keyword, item)
    return adj


def expand_keywords(keywords_):
    """
    The function adds plural and capitalized forms of words to the keywords list
    this ensures that the keyword will be located even if it is at the start of
    a sentence.

    Args:
        keywords_: A list of keywords.

    Returns:
        A list of original keywords with the addition of plurals, capitals, and
        the capitals of the plurals.
    """
    new_keywords = keywords_[:]
    for word in keywords_:
        new_keywords.append(word+"s")
        new_keywords.append(word.capitalize())
        new_keywords.append((word+"s").capitalize())
    return new_keywords


def find_adj_in_all_books(keywords):
    '''
    The function creates of a list of all the adjectives that
    are present in the books provided. It calls on find_adj_in_all_sentences

    Args:
        keywords: A string of keywords.

    Returns:
        A list consisting of adjectives.
    '''
    keywords = expand_keywords(keywords)
    adj = []
    for word in keywords:
        for book in os.listdir("BooksCleaned"):
            adj += (find_adj_in_all_sentences(word, f'BooksCleaned/{book}'))
        return adj


def find_adj_all_words_all_books(wordbank):
    '''
    This function creates a list of adjectives that are
    found both in the user provided word bank and in the source text.

    Args:
        wordbank: List of words that have been selected by the user. It is
        composed of a list of occupational category.

    Returns:
        List of adjectives that have been found in the books.
    '''
    adj_list = []
    for category_list in wordbank:
        adj_list.append(find_adj_in_all_books(category_list))
    return adj_list


def write_adj_list_to_file(wordbank, filename):
    """
    Find all adjectives for all lists in wordbank and write to file.

    Args:
        wordbank: a list of lists containing synonyms for each word.
        filename: the name of the file you wish to write your adjectives
        to.
    Returns:
        none
    """
    adj_list = find_adj_all_words_all_books(wordbank)
    with open(f'Outputs/{filename}.txt', 'w') as adj_file:
        for item in adj_list:
            adj_file.write(str(item) + "\n")


# Write all adjectives from all books into a file
if not os.path.exists("Outputs/all_adjectives_expanded.txt"):
    write_adj_list_to_file(word_bank, "all_adjectives_expanded")


def sentiment_countifier_individual(adjectives):
    """
    The function assigns positive, negative, and neutral
    score values to provided adjectives and then returns the values.

    Args:
        adjectives: a list of adjectives.

    Returns:
        A list of 3 integers which represent the average sentiment score of the
        adjectives. The 3 values are as follows:
        pos_score: The sentiment of the adjective on how positive it is.
        neu_score:The sentiment of the adjective on how neutral it is.
        neg_score:The sentiment of the adjective on how negative it is.
    """
    sia = SentimentIntensityAnalyzer()
    pos_scores = []
    neu_scores = []
    neg_scores = []
    for word in adjectives:
        sentiments = sia.polarity_scores(word)
        pos_scores.append(sentiments["pos"])
        neu_scores.append(sentiments["neu"])
        neg_scores.append(sentiments["neg"])
    pos_score = sum(pos_scores) / len(pos_scores)
    neu_score = sum(neu_scores) / len(neu_scores)
    neg_score = sum(neg_scores) / len(neg_scores)
    return [pos_score, neu_score, neg_score]


# Read adjectives from all_adjectives file, pack into a list of lists
with open("Outputs/all_adjectives_expanded.txt", 'r') as f:
    adjective_lists = []
    for line in f:
        adj_list_single_cat = line.strip()
        adj_list_single_cat = adj_list_single_cat.replace("'", "")
        divided_adj_list_single_cat = adj_list_single_cat[1:-1].split(",")
        adjective_lists.append(divided_adj_list_single_cat)
