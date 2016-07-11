# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 15:17:53 2016

@author: Tristan

run_this will load the Wikipedia xml file as an ElementTree,
find all the non-redirect articles with at least 300 characters,
take a reproducibly random subset of 10,000 articles,
get the titles and text of these articles
"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy
import random

def run_this():
    global root
    global indices
    global titles
    global text
    """This section contains the code to be executed"""
    root = parse_file()
    indices = get_article_indices(root)
    random.seed(8685)
    indices = random.sample(indices,10000)
    indices.sort()
    titles = get_titles(root,indices)
    text = get_text(root,indices)
    """end section"""

def parse_file():
    tree = ET.parse('simplewiki-20160701-pages-articles-multistream.xml')
    return tree.getroot()

def get_titles(root,indices):
    return [root[i][0].text for i in indices ]
    
def get_articles(root):
    indices = []
    for i in range(1,len(root.getchildren())):
        # Remove non-articles (ie help pages, categories, etc.)
        if root[i][1].text == "0":
            # Remove redirect articles
            redirect = root[i].find('{http://www.mediawiki.org/xml/export-0.10/}redirect')
            if redirect is None:
                # Remove articles with fewer than 300 characters
                # Yes, this does slow it down a lot.
                if( len(root[i][0].text) >= 300 ):
                    indices.append(i)
    return indices

def get_text(root,article_indices):
    text = []
    for child in [root[i] for i in article_indices]:
        for textnode in child.iter(tag ='{http://www.mediawiki.org/xml/export-0.10/}text'):
            text.append(textnode.text)
    return text
    
"""A few additional functions to characterize the articles"""
def get_length(text):
    #to execute:
    #(char_count, log_char, word_count, log_word) = get_length(text)
    char_count = [len(a) for a in text]
    log_char = numpy.log10(text_length)
    word_count = [len(a.split()) for a in text]
    log_word = numpy.log10(word_count)
    plt.hist(log_word)
    plt.ylabel("Number articles")
    plt.xlabel("Log number words")
    return char_count, log_char, word_count, log_word
