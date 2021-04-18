#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 20:53:19 2021

@author: czs
"""
from wordcloud import WordCloud
import nltk
nltk.download('punkt')
from nltk import wordnet
from textblob import TextBlob
from textblob import Word
import re
from ast import literal_eval
import os
import numpy as np
import sys
import csv
import tweepy
import matplotlib.pyplot as plt
import aylienapiclient
import pandas as pd
import requests
import json
import glob
from aylienapiclient import textapi 
from collections import Counter
'''***Part I***'''
consumer_key = "qMFAXWg1JjJsxkkJo3C2mc2Fm"
consumer_secret = "ZSWnZI8TUAYwQIcMo8ftpB0RpzQGscWVIRhupVeICbEiDHMWD3"
access_token = "1224377250184757248-FvfuO2CTQZMOgQfRw8a2U3DhL9m7vo"
access_token_secret = "E1LHRifyhwJJ4Xya1LnRmEHnjCfZleKbOXWldOdBO6QLs"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
query =["H&M"]
number=100000
  
results = api.search(
   lang="en",
   q=query,
   count=number,
   result_type="recent"
)
print("--- Gathered Tweets \n")
''''***Part II***'''
results_str=" ".join('%s' %id for id in results)
df = pd.DataFrame({'Tweet':results})
df.Tweet.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
df.Tweet.replace({r'[^a-zA-z\s]':''}, regex=True, inplace=True)
df.Tweet.replace({r'_':''}, regex=True, inplace=True)
df.to_csv("twitter.csv",index=False,sep=',')
with open('twitter.csv', 'r') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if i == 0:
            i = i+1
            continue
        temp = row[0].split('_json=',1)
        temp2 = temp[1].split("'text':",1)
        temp3 = temp2[1].split(", 'truncated'",1)
        comment = temp3[0][2:-1]
        comment = comment.replace(',','').lower()
        words = comment.split(' ')
        with open("test.txt","a") as f:
            for word in words:
                f.write(word+'    ')
            f.write('\n')
        i = i+1
''''***Part III***'''
STOPWORDS = ["an", "a", "the", "or", "and", "thou", "must", "that", "this", "self", "unless", "behind", "for", "which",
             "whose", "can", "else", "some", "will", "so", "from", "to", "by", "within", "of", "upon", "th", "with",
             "it"]
def _remove_stopwords(txt):
    words = txt.split()
    for i, word in enumerate(words):
        if word in STOPWORDS:
            words[i] = " "
    return (" ".join(words))
with open("test.txt", 'r', encoding='utf-8') as test_read:
    test_string = test_read.read()
test_split = str.split(test_string, sep=',')
print(test_split)
len(test_split)
doc_out = []
for k in test_split:
    cleantextprep = str(k)
    expression = "[^a-zA-Z ]"  
    cleantextCAP = re.sub(expression, '', cleantextprep)  
    cleantext = cleantextCAP.lower()  
    cleantext = _remove_stopwords(cleantext)
    bound = ''.join(cleantext)
    doc_out.append(bound)       
print(doc_out)
ndct = ''
with open('bl_negative.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        ndct = ndct + line
ndct = ndct.split('\n')
len(ndct)
pdct = ''
with open('bl_positive.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        pdct = pdct + line
pdct = pdct.split('\n')
len(pdct)
def decompose_word(doc):
    txt = []
    for word in doc:
        txt.extend(word.split())
    return txt
def wordcount(words, dct):
    counting = Counter(words)
    count = []
    for key, value in counting.items():
        if key in dct:
            count.append([key, value])
    return count
tokens = decompose_word(doc_out)
tokens_nltk = nltk.word_tokenize(str(doc_out))
comment_words = ' '
for token in tokens:
    comment_words = comment_words + token + ' '

print(len(comment_words))

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(comment_words)               
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig("wordcloud.png",format='png',dpi=200)
plt.show()
nwords = len(tokens)
nwc = wordcount(tokens, ndct) 
pwc = wordcount(tokens, pdct)
nwc1=" ".join('%s' %im for im in nwc).replace("'","")
pwc1=" ".join('%s' %im for im in pwc).replace("'","")
negwordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(nwc1)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(negwordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig("negwordcloud.png",format='png',dpi=200)
plt.show()
poswordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(pwc1)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(poswordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig("poswordcloud.png",format='png',dpi=200)
plt.show()

ntot, ptot = 0, 0
for i in range(len(nwc)):
    ntot += nwc[i][1]

for i in range(len(pwc)):
    ptot += pwc[i][1]
print('Positive words:')
for i in range(len(pwc)):
    print(str(pwc[i][0]) + ': ' + str(pwc[i][1]))
print('Total number of positive words: ' + str(ptot))
print('\n')
print('Percentage of positive words: ' + str(round(ptot / nwords, 4)))
print('\n')
print('Negative words:')
for i in range(len(nwc)):
    print(str(nwc[i][0]) + ': ' + str(nwc[i][1]))
print('Total number of negative words: ' + str(ntot))
print('\n')
print('Percentage of negative words: ' + str(round(ntot / nwords, 4)))





