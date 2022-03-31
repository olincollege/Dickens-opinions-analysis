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
    find_sentences_with_keyword
    
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
    '''
    The function adds plural and capitalized forms of words to the keywords list.
    
    Inputs:
        keywords_:  a list of keywords.
    
    Returns:
        new_keywords: a list of keywords.
    '''
    new_keywords=keywords_[:]
    for word in keywords_:
        new_keywords.append(word+"s")
        new_keywords.append(word.capitalize())
        new_keywords.append((word+"s").capitalize())
    return new_keywords

def find_adj_in_all_books(keywords):
    '''
    find_adj_in_all_books
    
    The function creates of a list of all the adjectives that
    are present in the books provided.
    
    Inputs:
        Keywords: A string of keywords
        
    Returns:
        Adj: A list consisting of adjectives
    '''
    keywords=expand_keywords(keywords)
    adj=[]
    for word in keywords:
        for book in os.listdir("BooksCleaned"):
            adj+=(find_adj_in_all_sentences(word,f'BooksCleaned/{book}')) 
        return(adj)
        
def find_adj_all_words_all_books(wordbank):
    '''
    find_adj_all_words_all_books
    
    This function creates a list of adjectives that are
    found both in the user provided word bank and in the source text.
    
    Inputs:
        Wordbank: List of words that have been selected by the user. It is composed of a list of occupational category.
    
    Returns:
        Adj_list: List of adjectives that have been found in the books. 
    '''
    adj_list = []
    for list in wordbank:
        adj_list.append(find_adj_in_all_books(list))
    return adj_list


def sentiment_countifier_individual(adjectives):
    '''
    sentiment_countifier_individual
    
    The function assigns positive, negative, and neutral 
    score values to provided adjectives and then returns the values.
    
    Inputs:
        Adjectives: a list of adjectives.
    
    Returns:
        Pos_score: The sentiment of the adjective on how positive it is.
        Neu_scores:The sentiment of the adjective on how neutral it is.
        Neg_scores:The sentiment of the adjective on how negative it is.
    '''
    sia = SentimentIntensityAnalyzer()
    pos_scores=[]    
    neu_scores=[]    
    neg_scores=[] 
    for word in adjectives:    
        sentiments = sia.polarity_scores(word)
        print(sentiments)
        pos_scores.append(sentiments["pos"])
        neu_scores.append(sentiments["neu"])
        neg_scores.append(sentiments["neg"])
    pos_score= sum(pos_scores) / len(pos_scores)
    neu_score= sum(neu_scores) / len(neu_scores)
    neg_score= sum(neg_scores) / len(neg_scores)    
    return [pos_score,neu_score,neg_score]

word_categories = ["lawyer", "nurse", "female servant", "tailor", "governess",
"clerk", "craftsman", "businessman", "street peddlar", "orphan",
"male servant", "banker", "criminal", "navvy", "nightman", "farmer", 
"innkeeper", "miner", "waiter", "clergyman", "clerk", "washerwoman", 
"governess", "student", "doctor", "soldier", "high-rank military", "policeman",
"fisherman", "shoolteacher", "politician"]

print(len(word_categories))
