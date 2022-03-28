from gettext import find
import nltk
import os

sample_text = "It was a tall tree. The squirrel lost its tiny hat. It had to \
    climb down the tree to find the hat. 'That's unfortunate!'"
sample_tokens = nltk.word_tokenize(sample_text)

def test_find_sentences_with_keyword():
    """
    Test that the function corectly finds all sentences containing the keyword
    """
    assert find_sentences_with_keyword("hat", sample_tokens) == ["The squirrel \
        lost its tiny hat.","It had to climb down the tree to find the hat."]

def test_find_occurances_of_keyword():
    """
    Test that the function finds the indexes of all strings that match the
    keyword exactly
    """
    # Test a single word that occurs once in a string
    assert find_occurances_of_keyword("squirrel", sample_tokens) == [7]
    # Test that a lowercase keyword is found only in lowercase form
    assert find_occurances_of_keyword("the", sample_tokens) == [18, 22]
    # Test that words inside of other words are not counted as occurances
    assert find_occurances_of_keyword("hat", sample_tokens) == [11, 23]
    # Test that searching for a word not in the string returns

def test_find_adjectives():
    pass

def test_find_words_that_describe_keyword():
    pass

def test_look_for_adjectives():
    pass

def test_find_adj_in_all_sentences():
    pass

def test_expand_keywords():
    pass