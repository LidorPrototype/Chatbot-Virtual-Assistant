# pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
import torch
# print(torch.__version__)
import nltk  # nltk.download('punkt')    -->     Download it once
from nltk.stem.porter import PorterStemmer
import numpy as np


stemmer = PorterStemmer()


def tokenize(sentence):  # spilling sentence into an array of words
    return nltk.word_tokenize(sentence)


def stem(word):  # giving the root of the $word
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w, in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag
















































