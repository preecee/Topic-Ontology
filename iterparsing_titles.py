# -*- coding: utf-8 -*-
"""
Created on 24 Jul

@author: Diya

run_this will parse the Wikipedia xml file,
find all the non-redirect articles,
take a reproducible random subset of 10000 articles,
get the titles and text of these articles,
and return a pandas dataframe
"""

#import xml.etree.ElementTree as ET
from lxml import etree
import matplotlib.pyplot as plt
import numpy
import random
import pandas as pd
import wikipedia as wiki
import sys
import datetime
import pickle

def api_to_df(titlefile='en_wikipedia_titles.pkl', nsample=10000, subname=''): 
    with open("iterparsing_titles"+subname+".log", "a") as logfile:
        logfile.write(str(datetime.datetime.today())+'\n'+titlefile+'\n'+str(nsample)+'\n')
    titles =  get_titles(titlefile) 
    random.seed(8685)
    titles = random.sample(titles, nsample)
    newtitles, text, links = get_text(titles, subname)
    with open(titlefile+'_df_'+str(nsample)+subname+'_comp.pkl','wb') as f:
        pickle.dump(newtitles,f)
        pickle.dump(text,f)
        pickle.dump(links,f)
    df = get_dataframe(newtitles, text, links)
    df.to_pickle(titlefile+'_df_'+str(nsample)+subname+'.pkl')
    with open("iterparsing_titles"+subname+".log", "a") as logfile:
        logfile.write("Complete at " + str(datetime.datetime.today()) + '\n')
    return df, newtitles, text, links

def get_text(input_titles, subname):
    titles = []
    text = []
    links = []
    counter = 0
    for title in input_titles: 
        try:
            page = wiki.page(title)
            plinks = page.links
            text.append(page.summary)
            titles.append(title)
            links.append(plinks)
            counter += 1
            if counter % 100 == 0:
                with open("iterparsing_titles"+subname+".log", "a") as logfile:
                    logfile.write(str(counter) + " titles have data at " + str(datetime.datetime.today())+'\n')
        except Exception:
            with open("iterparsing_titles"+subname+".log", "a") as logfile:
                logfile.write(title + " : does not appear to have viable summary or internal links. Maybe it's a stub?\n")
            pass
    return titles, text, links

def get_titles(titlefile):
    titles = pickle.load(open(titlefile,"rb"))
    return titles

def get_dataframe(titles, text, links):
    data=pd.DataFrame(index=range(len(text)),columns=['title','text','links'])
    data['title']=titles
    data['text']=text
    data['links']=links
    return data

"""A few additional functions to characterize the articles"""
def get_length(text):
    #to execute:
    #(char_count, log_char, word_count, log_word) = get_length(text)
    char_count = [len(a) for a in text]
    log_char = numpy.log10(char_count)
    word_count = [len(a.split()) for a in text]
    log_word = numpy.log10(word_count)
    plt.hist(log_word)
    plt.ylabel("Number articles")
    plt.xlabel("Log number words")
    return char_count, log_char, word_count, log_word
