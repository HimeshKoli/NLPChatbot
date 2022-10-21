import nltk
#nltk.download('punkt')
import numpy as np

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# in tokenize we will seperate each word in sentence and make a list
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# in stemming we use porterstemmer which removes most suffixes and shortens the word as much as possible to make it understandable
def stemming(word):
    return stemmer.stem(word.lower()) # to lower any capitalize word

# a = "What information do I need to provide?"
# print(a)

# a = tokenize(a)
# print(a)

# stemmed_words = [stemming(w) for w in a]

# print(stemmed_words)

# words = ['Organization', 'oragnizes', 'organizing', 'Organize']

# stemmed_words1 = [stemming(w) for w in words]
# print(stemmed_words1)


# in bag of words we give position of each word in sentence so that machine recognizes
'''
tokenized_sentence = ['hello', 'how', 'are', 'you']
all_words = ['hi', 'hello', 'i', 'you', 'thank', 'cool', 'bye']
bag_of_words = [0,   1,      0,    1,      0,      0,      0]
'''
# so basically the parameters tokenized_sentence is our new tokenized sentence with each word in that sentence seperated with the help of tokenizer and 2nd parameter all_words is our list
# which we already made for our patterns

# so we look for every word from our new tokenized sentence in all_words and if the word is present in all_words then we number it as 1, now we need to implement this in code form

def bag_of_words(tokenized_sentence, all_words):

    tokenized_sentence = [stemming(p) for p in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)  # we first initiate all numbering of words as zero with the help of numpy np.zeros function
    for idx, p in enumerate(all_words):  # all the tokenize words list of pattern will get an index with enumerate and below
        if p in tokenized_sentence:  # here we have used tokenized_sentence as parameter and when we use this bag_of_words function in training_data.py there are parameter is pattern_sentence
            bag[idx] = 1.0

    return bag

# sent = ['hello', 'how', 'are', 'you']
# words = ['hi', 'hello', 'i', 'you', 'thank', 'cool', 'bye']
# bang = bag_of_words(sent, words)
# print(bang) # working