
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re 
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def Tokenize(sentence):
    query = sentence.lower()
    tokens = word_tokenize(query)
    return tokens

def POS_Tagging(tokens):
    parts_of_speech = nltk.pos_tag(tokens)

    return parts_of_speech

def FilterStopwords(tokens):
    stop_words = set(stopwords.words('english'))

    filtered_tokens = []
    pos_array = []
    for token,pos in tokens:
        if(token in stop_words):
            continue
        temp = (token,pos)
        filtered_tokens.append(temp)

    return filtered_tokens

def LemmatizeTokens(tokens):
    lemmatizer = WordNetLemmatizer()

    final_words = []
    adjectives = ["JJR","JJ","JJS"]
    nouns = ["NN","NNS","NNP","NNPS"]
    verbs = ["VB","VBD","VBG","VBN","VBP","VBZ"]
    adverbs = ["RB","RBR","RBS"]
    for word in tokens:
        pos = "n"

        if word[1] in adjectives:
            pos = "a"
        elif word[1] in nouns:
            pos = "n"
        elif word[1] in verbs:
            pos = "v"
        elif word[1] in adverbs:
            pos = "r"

        final_words.append(lemmatizer.lemmatize(word[0],pos))

    return final_words

def Process(query):
    tokens = Tokenize(query)
    tokens = POS_Tagging(tokens)
    tokens = FilterStopwords(tokens)
    tokens = LemmatizeTokens(tokens)

    return tokens


def ProcessCorpus(corpus):
    tokens = {}
    for key,value in corpus.items():
        tokens[key] = Process(value)

    return tokens

if __name__ == "__main__":
    print(Process("How Big Is The City Of Rome"))
    