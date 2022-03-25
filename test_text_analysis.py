import nltk
import os

sample_text = "It was a tall tree. The squirrel lost its tiny hat. It had to \
    climb down the tree to find the hat. 'That's unfortunate!'"
testing_text = nltk.word_tokenize(sample_text)

def test_find_sentences_with_keyword():
    """
    Test that the function corectly finds all sentences containing the keyword
    """
    assert find_sentences_with_keyword("hat", testing_text) == ["The squirrel \
        lost its tiny hat.","It had to climb down the tree to find the hat."]

def test_find_occurances_of_keyword():
    pass

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