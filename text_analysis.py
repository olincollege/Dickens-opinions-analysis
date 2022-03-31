import nltk
import os
import spacy
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


from WordBank import word_bank

def find_occurances_of_keyword(keyword,text):
    """
    Find_occurances_of_keywords
    Find occurrences of the selected keyword within the text provided 
    then return a list of indexed occurrences of the word within the text.

    Args: 
        Keyword: String, the selected keyword.
        Text: A tokenized text in the form of a list of strings.

    Returns:
        list_of_indexes: Returns a list of indexes for each occurance of the
        keyword.
    """
    list_of_indexes=[]
    for index,word in enumerate(text):
        if keyword == word:
            list_of_indexes.append(index)
    return list_of_indexes

def find_sentences_with_keyword(keyword, text):
    """
    Find the sentence that contextualizes the occurence of a keyword and return a list
    of indices that represent the range of each sentence containing the keyword.
    
    Args:
        keyword: a string representing a word to contextualize in a sentence.
        text: a tokenized text given as a list of strings of words and punctuation.
        
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
    sentences=[]
    for range_ in sentence_ranges:
        new_sentence=TreebankWordDetokenizer().detokenize((text[range_[0]:range_[1]]))
        sentences.append(new_sentence.replace(" ’ ", "’"))
    return sentences

def look_for_adjectives(word,sentence):
    """
    Look_for_adjectives
    This function parses through a provided sentence and identifies
    if the word is an adjective. The function then returns a list of adjectives.
    Inputs:
        Word: String representing the target keyword to be described.
        Sentence: A string consisting of the provided sentence.
    Returns:
        Adjectives: a list of strings representing adjectives.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    adjectives=[]
    for token in doc:
        #print(token.text +" "+token.dep_+" "+token.head.text+" "+token.pos_)
        working_token=token
        while working_token.dep_ != "ROOT":
            if working_token.head.text==word and (token.pos_==("ADJ")):
                adjectives.append(token.text)
                break
            if working_token.head.text==working_token.text:
                break
            working_token=working_token.head
    return adjectives

def find_adj_in_all_sentences(keyword,path):
    '''
    Find_adj_in_all_sentences
    The function opens a file of text, parses through the text,
    and adds any adjectives to a string.
    Inputs:
        Keyword: String of a set keyword
        Path: a string of a path to a file.
    Returns
        Adj: list of adjectives

    '''
    with open(path) as book:
        contents = book.read()
        text = nltk.word_tokenize(contents)
        #parts_of_speech = nltk.pos_tag(tokens)
    adj=[]
    for item in find_sentences_with_keyword(keyword, text):
        adj+=look_for_adjectives(keyword,item)
    return adj

def expand_keywords(keywords_):
    new_keywords=keywords_[:]
    for word in keywords_:
        new_keywords.append(word+"s")
        new_keywords.append(word.capitalize())
        new_keywords.append((word+"s").capitalize())
    return new_keywords

def find_adj_in_all_books(keywords):
    keywords=expand_keywords(keywords)
    adj=[]
    for word in keywords:
        for book in os.listdir("BooksCleaned"):
            adj+=(find_adj_in_all_sentences(word,f'BooksCleaned/{book}')) 
        return(adj)
        
def find_adj_all_words_all_books(wordbank):
    adj_list = []
    for list in wordbank:
        adj_list.append(find_adj_in_all_books(list))
    return adj_list


def sentiment_countifier_individual(adjectives):
    sia = SentimentIntensityAnalyzer()
    pos_scores=[]    
    neu_scores=[]    
    neg_scores=[] 
    for word in adjectives:    
        sentiments = sia.polarity_scores(word)
        pos_scores.append(sentiments["pos"])
        neu_scores.append(sentiments["neu"])
        neg_scores.append(sentiments["neg"])
    pos_score= sum(pos_scores) / len(pos_scores)
    neu_score= sum(neu_scores) / len(neu_scores)
    neg_score= sum(neg_scores) / len(neg_scores)    
    return [pos_score,neu_score,neg_score]


