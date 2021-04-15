# pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
# pip install nltk      -->     Natural Language Tool Kit
# pip install numpy
# pip install tensorflow
import torch    # print(torch.__version__)
import nltk     # nltk.download('punkt')    -->     Download it once
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tensorflow
import random
import json


stemmer = LancasterStemmer()

with open("intents.json") as file:
    data = json.load(file)

print(data)
