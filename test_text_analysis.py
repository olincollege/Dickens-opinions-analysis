"""
Test helper funtions in text_analysis.
"""
import nltk
import os

from text_analysis import *

sample_text1 = "It was a tall tree. The squirrel lost its tiny hat. It had to \
    climb down the tree to find the hat. 'That's unfortunate!'"
sample_tokens1 = nltk.word_tokenize(sample_text1)
sample_text2 = "Miriam bought a deliciously moist chapstick from Trader \
    Johan's. Malvina's mother's crispy crackers make a distracted \
    Miriam very happy."
sample_tokens2 = nltk.word_tokenize(sample_text2)
sample_text3 = "She had sharp and hairy elbows."
sample_tokens3 = nltk.word_tokenize(sample_text3)


def test_find_occurances_of_keyword():
    """
    Test that the function finds the indexes of all strings that match the
    keyword exactly
    """
    # Test a single word that occurs once in a string
    assert find_occurances_of_keyword("squirrel", sample_tokens1) == [7]
    # Test that a lowercase keyword is found only in lowercase form
    assert find_occurances_of_keyword("the", sample_tokens1) == [18, 22]
    # Test that words inside of other words are not counted as occurances
    assert find_occurances_of_keyword("hat", sample_tokens1) == [11, 23]
    # Test that searching for a word not in the string returns an empty string
    assert find_occurances_of_keyword("bread", sample_tokens1) == []


def test_find_sentences_with_keyword():
    """
    Test that the function correctly finds all sentences containing the keyword
    """
    # Check for a single sentence string
    assert find_sentences_with_keyword("sharp", sample_tokens3) == [
        "She had sharp and hairy elbows."]
    # Check for a a multiple sentence string
    assert find_sentences_with_keyword("crackers", sample_tokens2) == \
        ["Malvina's mother's crispy crackers make a distracted Miriam very "
        + "happy."]
    # Check for a a multiple sentence string, word in multiple sentences
    assert find_sentences_with_keyword("Miriam", sample_tokens2) == [
        "Miriam bought a deliciously moist chapstick from Trader Johan's.",
        "Malvina's mother's crispy crackers make a distracted Miriam very"
        + " happy."]


def test_look_for_adjectives():
    """
    Test the spacy implementation of adjective finder
    """
    # Test find adjectives for a single word
    assert look_for_adjectives("hat", "The squirrel lost its tiny hat.") == \
        ["tiny"]
    # Test find adjectives in a string with multiple other adjectives.
    assert look_for_adjectives("Miriam", "Malvina's mother's crispy crackers \
        make a distracted Miriam very happy.") == ["distracted"]
    # Test that a word that is not a noun returns no adjectives.
    assert look_for_adjectives("It", "It was a tall tree.") == []
    assert look_for_adjectives("moist", "Miriam bought a deliciously moist \
        chapstick from Trader Johan's.") == []
    # Check that an adjective separated by one word from keyword is found.
    assert look_for_adjectives("elbows", "She had sharp and hairy elbows.") == \
        ["sharp", "hairy"]


def test_expand_keywords():
    """
    Check that the function returns the regular plural and capitalized version\
    of a word
    """
    # Check that a sinngle keyword is expanded.
    assert expand_keywords(["bath"]) == ["bath", "baths", "Bath", "Baths"]
    # Check that multiple keywords are expanded.
    assert expand_keywords(["house", "frog"]) == ["house", "frog", "houses",
                                                 "House", "Houses", "frogs",
                                                 "Frog", "Frogs"]
