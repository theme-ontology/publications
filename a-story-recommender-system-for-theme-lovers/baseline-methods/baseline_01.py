# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 17:30:49 2018

@author: sergio
"""
import html2text
import codecs
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.porter import *
from collections import defaultdict
from gensim import corpora

episodes=(
"tos0x01","tos1x01","tos1x02","tos1x03","tos1x04","tos1x05","tos1x06","tos1x07","tos1x08","tos1x09","tos1x10","tos1x11","tos1x12","tos1x13","tos1x14","tos1x15","tos1x16","tos1x17","tos1x18",
"tos1x19","tos1x20","tos1x21","tos1x22","tos1x23","tos1x24","tos1x25","tos1x26","tos1x27","tos1x28","tos1x29","tos2x01","tos2x02","tos2x03","tos2x04","tos2x05","tos2x06","tos2x07","tos2x08",
"tos2x09","tos2x10","tos2x11","tos2x12","tos2x13","tos2x14","tos2x15","tos2x16","tos2x17","tos2x18","tos2x19","tos2x20","tos2x21","tos2x22","tos2x23","tos2x24","tos2x25","tos2x26","tos3x01",
"tos3x02","tos3x03","tos3x04","tos3x05","tos3x06","tos3x07","tos3x08","tos3x09","tos3x10","tos3x11","tos3x12","tos3x13","tos3x14","tos3x15","tos3x16","tos3x17","tos3x18","tos3x19","tos3x20",
"tos3x21","tos3x22","tos3x23","tos3x24","tas1x01","tas1x02","tas1x03","tas1x04","tas1x05","tas1x06","tas1x07","tas1x08","tas1x09","tas1x10","tas1x11","tas1x12","tas1x13","tas1x14","tas1x15",
"tas1x16","tas2x01","tas2x02","tas2x03","tas2x04","tas2x05","tas2x06","tng1x01","tng1x02","tng1x03","tng1x04","tng1x05","tng1x06","tng1x07","tng1x08","tng1x09","tng1x10","tng1x11","tng1x12",
"tng1x13","tng1x14","tng1x15","tng1x16","tng1x17","tng1x18","tng1x19","tng1x20","tng1x21","tng1x22","tng1x23","tng1x24","tng1x25","tng1x26","tng2x01","tng2x02","tng2x03","tng2x04","tng2x05",
"tng2x06","tng2x07","tng2x08","tng2x09","tng2x10","tng2x11","tng2x12","tng2x13","tng2x14","tng2x15","tng2x16","tng2x17","tng2x18","tng2x19","tng2x20","tng2x21","tng2x22","tng3x01","tng3x02",
"tng3x03","tng3x04","tng3x05","tng3x06","tng3x07","tng3x08","tng3x09","tng3x10","tng3x11","tng3x12","tng3x13","tng3x14","tng3x15","tng3x16","tng3x17","tng3x18","tng3x19","tng3x20","tng3x21",
"tng3x22","tng3x23","tng3x24","tng3x25","tng3x26","tng4x01","tng4x02","tng4x03","tng4x04","tng4x05","tng4x06","tng4x07","tng4x08","tng4x09","tng4x10","tng4x11","tng4x12","tng4x13","tng4x14",
"tng4x15","tng4x16","tng4x17","tng4x18","tng4x19","tng4x20","tng4x21","tng4x22","tng4x23","tng4x24","tng4x25","tng4x26","tng5x01","tng5x02","tng5x03","tng5x04","tng5x05","tng5x06","tng5x07",
"tng5x08","tng5x09","tng5x10","tng5x11","tng5x12","tng5x13","tng5x14","tng5x15","tng5x16","tng5x17","tng5x18","tng5x19","tng5x20","tng5x21","tng5x22","tng5x23","tng5x24","tng5x25","tng5x26",
"tng6x01","tng6x02","tng6x03","tng6x04","tng6x05","tng6x06","tng6x07","tng6x08","tng6x09","tng6x10","tng6x11","tng6x12","tng6x13","tng6x14","tng6x15","tng6x16","tng6x17","tng6x18","tng6x19",
"tng6x20","tng6x21","tng6x22","tng6x23","tng6x24","tng6x25","tng6x26","tng7x01","tng7x02","tng7x03","tng7x04","tng7x05","tng7x06","tng7x07","tng7x08","tng7x09","tng7x10","tng7x11","tng7x12",
"tng7x13","tng7x14","tng7x15","tng7x16","tng7x17","tng7x18","tng7x19","tng7x20","tng7x21","tng7x22","tng7x23","tng7x24","tng7x25","tng7x26","voy1x01","voy1x02","voy1x03","voy1x04","voy1x05",
"voy1x06","voy1x07","voy1x08","voy1x09","voy1x10","voy1x11","voy1x12","voy1x13","voy1x14","voy1x15","voy1x16","voy2x01","voy2x02","voy2x03","voy2x04","voy2x05","voy2x06","voy2x07","voy2x08",
"voy2x09","voy2x10","voy2x11","voy2x12","voy2x13","voy2x14","voy2x15","voy2x16","voy2x17","voy2x18","voy2x19","voy2x20","voy2x21","voy2x22","voy2x23","voy2x24","voy2x25","voy2x26","voy3x01",
"voy3x02","voy3x03","voy3x04","voy3x05","voy3x06","voy3x07","voy3x08","voy3x09","voy3x10","voy3x11","voy3x12","voy3x13","voy3x14","voy3x15","voy3x16","voy3x17","voy3x18","voy3x19","voy3x20",
"voy3x21","voy3x22","voy3x23","voy3x24","voy3x25","voy3x26","voy4x01","voy4x02","voy4x03","voy4x04","voy4x05","voy4x06","voy4x07","voy4x08","voy4x09","voy4x10","voy4x11","voy4x12","voy4x13",
"voy4x14","voy4x15","voy4x16","voy4x17","voy4x18","voy4x19","voy4x20","voy4x21","voy4x22","voy4x23","voy4x24","voy4x25","voy4x26","voy5x01","voy5x02","voy5x03","voy5x04","voy5x05","voy5x06",
"voy5x07","voy5x08","voy5x09","voy5x10","voy5x11","voy5x12","voy5x13","voy5x14","voy5x15","voy5x16","voy5x17","voy5x18","voy5x19","voy5x20","voy5x21","voy5x22","voy5x23","voy5x24","voy5x25",
"voy5x26","voy6x01","voy6x02","voy6x03","voy6x04","voy6x05","voy6x06","voy6x07","voy6x08","voy6x09","voy6x10","voy6x11","voy6x12","voy6x13","voy6x14","voy6x15","voy6x16","voy6x17","voy6x18",
"voy6x19","voy6x20","voy6x21","voy6x22","voy6x23","voy6x24","voy6x25","voy6x26","voy7x01","voy7x02","voy7x03","voy7x04","voy7x05","voy7x06","voy7x07","voy7x08","voy7x09","voy7x10","voy7x11",
"voy7x12","voy7x13","voy7x14","voy7x15","voy7x16","voy7x17","voy7x18","voy7x19","voy7x20","voy7x21","voy7x22","voy7x23","voy7x24","voy7x25","voy7x26",        
        )

stemmer=PorterStemmer()
to_remove=set(stopwords.words('english')+[".",",",":",";","?","[","]","(",")","-","!","http"])
frequency = defaultdict(int)

texts=[]
for episode in episodes[:20]:
    print(episode)
    series=episode[:3]
    input_file=codecs.open("transcripts/"+series+"/"+episode+".html","r","utf-8")
    html=input_file.read()
    input_file.close()
    text=html2text.html2text(html).lower().replace("**","")
    tokens=[stemmer.stem(t) for t in word_tokenize(text) if not t in to_remove and len(t)<20 and len(t)>2 and t.isalpha()]
    for token in text:
        frequency[token]+=1
    texts.append(text)
print()

# remove words that appear only once
texts = [[token for token in text if frequency[token] > 1] for text in texts]
dictionary = corpora.Dictionary(texts)
print(dictionary)
corpus=[dictionary.doc2bow(text) for text in texts]  
print(corpus[0])
print("done")
    
