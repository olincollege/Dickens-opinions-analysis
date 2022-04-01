from WordBank import word_categories
from collections import Counter
import collections
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('stopwords')
from text_analysis import sentiment_countifier_individual
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # Read adjectives from all_adjectives file, pack into a list of lists
with open("Outputs/all_adjectives_expanded.txt", 'r') as f:
    adjective_lists = []
    for line in f:
        adj_list_single_cat = line.strip()
        adj_list_single_cat = adj_list_single_cat.replace("'", "")
        divided_adj_list_single_cat = adj_list_single_cat[1:-1].split(",")
        adjective_lists.append(divided_adj_list_single_cat)

def sentiment_score_all_adjectives(all_adjective_lists):
    sentiment_score_list = []
    for list in all_adjective_lists:
        sentiments = sentiment_countifier_individual(list)
        sentiment_score_list.append(sentiments)
    return sentiment_score_list


# Create a bar graph for sentiments scores in all categories
def plot_scores_all_categories():
    """
    Create a bar graph for sentiment scores in all categories
    """
    scores_list = sentiment_score_all_adjectives(adjective_lists)
    trimmed_word_categories2=[]
    for word,index in enumerate(word_categories):
        trimmed_word_categories2.append([word,index])
    trimmed_word_categories=[]
    trimmed_word_categories3=[]
    for i, category in enumerate(word_categories):
       if adjective_lists[i] != [""]:
            trimmed_word_categories.append(trimmed_word_categories2[i])
            trimmed_word_categories3.append(trimmed_word_categories2[i][1])

    number_of_categories = len(trimmed_word_categories)
    ind = np.arange(number_of_categories)
    width = .25

    pos_scores = []
    neu_scores = []
    neg_scores = []

    for category_number, category in enumerate(trimmed_word_categories):
        pos_scores.append(scores_list[category[0]][0])
        neu_scores.append(scores_list[category[0]][1])
        neg_scores.append(scores_list[category[0]][2])
    

    bar1 = plt.bar(ind, pos_scores, width, color = 'g')
    bar2 = plt.bar(ind+width, neu_scores, width, color='b')
    bar3 = plt.bar(ind+width*2, neg_scores, width, color = 'r')

    plt.xlabel("Category")
    plt.ylabel("Sentiment Scores")
    plt.title("Sentiment Scores by Category")

    plt.xticks(ind+width, trimmed_word_categories3, rotation='vertical')
    plt.legend( (bar1, bar2, bar3), ('pos', 'neu', 'neg') )
    plt.show()

def plot_sentiments_gender_categories():
    """
    Create a bar graph for six word categories paired by gender.
    """
    gender_categories_indexes = [0,1,15,17,18,21]
    gender_categories = [word_categories[w] for w in gender_categories_indexes]


    scores_list = sentiment_score_all_adjectives(adjective_lists)

    number_of_categories = len(gender_categories)
    ind = np.arange(number_of_categories)
    width = .25

    pos_scores = []
    neu_scores = []
    neg_scores = []

    for category_number, category in enumerate(gender_categories):
        pos_scores.append(scores_list[gender_categories_indexes[category_number]][0])
        neu_scores.append(scores_list[gender_categories_indexes[category_number]][1])
        neg_scores.append(scores_list[gender_categories_indexes[category_number]][2])
    
    bar1 = plt.bar(ind, pos_scores, width, color = 'g')
    bar2 = plt.bar(ind+width, neu_scores, width, color='b')
    bar3 = plt.bar(ind+width*2, neg_scores, width, color = 'r')

    plt.xlabel("Category")
    plt.ylabel("Sentiment Scores")
    plt.title("Sentiment Scores by Category")

    plt.xticks(ind+width, gender_categories, rotation='vertical')
    plt.legend( (bar1, bar2, bar3), ('pos', 'neu', 'neg') )
    plt.show()

def make_word_clouds_all_categories():
    """
    Create a word cloud of all adjectives for all word categories.
    """
    for index,list in enumerate(adjective_lists):
        if list==[""]:
            print(f'{word_categories[index].capitalize()} had no matches.')
            continue
        string_version=" ".join(list)
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(string_version)
    
        # plot the WordCloud image                      
        plt.figure(figsize = (8, 8), facecolor = None)
        fig = plt.figure()
        ax = fig.add_subplot()
        fig.subplots_adjust(top=.85)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        ax.set_title(word_categories[index].capitalize(), fontsize=14,
        fontweight='bold', pad=15)
        plt.show()
    
        #Creating list of 5 most common words 
        words = nltk.tokenize.word_tokenize(" ".join(list))
        fdist = FreqDist(w.lower() for w in words)
        most_common= fdist.most_common(5)
        print(f'The 5 most common adjectives are: {most_common}')
