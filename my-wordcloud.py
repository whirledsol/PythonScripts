#!/usr/bin/env python3
"""
wordcloud.py
Created:
@author: Will Rhodes

USAGE:
./my-wordcloud.py -i ./assets/battlestar_scripts_cleaned.txt -b white -f --mask ./assets/battlestar.jpg -o ./assets/battlestar_cloud.jpg
"""

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import argparse
import re
import numpy as np

MYSTOPWORDS = ['oh','the','be','to','of','and','a','in','that','have','i','it','for','not','on','with','he','as','you','do','at','this','but','his','by','from','they','we','say','her','she','or','an','will','my','one','all','would','there','their','what','so','up','out','if','about','who','get','which','go','me','when','make','can','like','time','no','just','him','know','take','person','into','year','your','good','some','could','them','see','other','than','then','now','look','only','come','its','over','think','also','back','after','use','two','how','our','work','first','well','way','even','new','want','because','any','these','give','day','most','us','ok','okay','mr','dr','ms','mrs','miss','right','left','gonna','need','got','thing','tell','going','let','really']

def start():
    parser = argparse.ArgumentParser(description='generate word cloud from file')
    parser.add_argument('-i','--input', type=str, help='path to file',dest='input', required=True)
    parser.add_argument('-o','--output', type=str, help='path to save file',dest='output')
    parser.add_argument('-f','--filter', help='filter out common words',dest='filter', action='store_true')
    parser.add_argument('-c','--collocations', help='include phrases/bigrams',dest='collocations', action='store_true')
    parser.add_argument('-b','--background', type=str, help='background color',dest='background', default="black")
    parser.add_argument('-m','--max-words', type=int, help='max number of words',dest='maxwords', default=1000)
    parser.add_argument('--width', type=int, help='cloud width',dest='width', default=1920*2.5)
    parser.add_argument('--height', type=int, help='cloud height',dest='height', default=1080*2.5)
    parser.add_argument('--mask', type=str, help='mask path',dest='mask', default=None)
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        #get contents
        contents = f.read()
        cloud(args,contents)

def cloud(args,text):
    
    #clean text
    text = text.lower()
    text = re.sub('[^A-Za-z0-9\-\' ]', '', text)
    text = re.sub('\\n|\\t|  ', ' ', text)
    #print(text)

    #other options
    stopwords = set(list(STOPWORDS) + MYSTOPWORDS) if args.filter else None

    if args.mask:
        mask = np.array(Image.open(args.mask))

    # Create and generate a word cloud image:
    wordcloud = WordCloud(stopwords=stopwords, background_color=args.background, mode="RGB", max_words=args.maxwords, width=args.width, height=args.height,normalize_plurals=True,repeat=False,collocations=args.collocations,margin=10,mask=mask,contour_width=2).generate(text)

    if args.output is not None:
        wordcloud.to_file(args.output)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    if mask is not None:
        #plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
        pass
    plt.axis("off")
    plt.show()


if  __name__ =='__main__':start()
