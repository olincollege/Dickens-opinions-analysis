
import nltk
import os

sample_text1 = "It was a tall tree. The squirrel lost its tiny hat. It had to \
    climb down the tree to find the hat. 'That's unfortunate!'"
sample_tokens1 = nltk.word_tokenize(sample_text1)
sample_text2 = "Miriam bought a deliciously moist chapstick from Trader \
    Johan's. Malvina's mother's crispy crackers make a distracted \
    Miriam very happy."
sample_tokens2 = nltk.word_tokenize(sample_text2)

def test_find_sentences_with_keyword():
    """
    Test that the function correctly finds all sentences containing the keyword
    """
    assert find_sentences_with_keyword("hat", sample_tokens1) == ["The squirrel \
        lost its tiny hat.","It had to climb down the tree to find the hat."]

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

def test_find_adjectives():
    """
    Check that the function correctly identifies the indexes all adjectives in
    the string that occur befor the keyword
    """
    parts_of_speech1 = nltk.pos_tag(sample_tokens1)
    parts_of_speech2 = nltk.pos_tag(sample_tokens2)
    # Test find adjectives for a single word
    assert find_adjectives([4], parts_of_speech) == ["tall"]
    # Test find adjectives for multiple words
    assert find_adjectives([4, 11], parts_of_speech) == ["tall", "tiny"]
    # Test find adjectives in a string with multiple other adjectives.
    assert find_adjectives([18], parts_of_speech2) == ["crispy"]
    # Test that a word that is not a noun returns no adjectives.
    assert find_adjectives([1], parts_of_speech2) == []

def test_look_for_adjectives():
    """
    Test the spacy implementation of adjective finder
    """
    # Test find adjectives for a single word
    assert find_adjectives("tree", sample_text1[0:12]) == ["tall"]
    # Test find adjectives in a string with multiple other adjectives.
    assert find_adjectives("crackers", sample_text2[12:26]) == ["crispy"]
    # Test that a word that is not a noun returns no adjectives.
    assert find_adjectives("It", sample_text1[6:12]) == []
    assert find_adjectives("moist", sample_text2[0:11]) == []
    # Check that an adjective separated by one word from keyword is found.
    assert find_adjectives("Miriam", sample_text2[12:27]) == ["happy"]


def test_expand_keywords():
    """ 
    Check that the function returns the regular plural and capitalized version\
    of a word
    """
    # Check that a sinngle keyword is expanded.
    assert expand_keywords(["bath"]) == ["bath", "Bath", "baths", "Baths"]
    # Check that multiple keywords are expanded.
    assert expand_keywords(["house", "frog"]) == ["house", "frog", "House",\
         "houses", "Houses", "Frog", "frogs", "Frogs"]
    pass