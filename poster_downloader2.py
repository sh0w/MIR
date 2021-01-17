#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse

from google_images_download import google_images_download   #importing the library
import pickle

import numpy as np
import pandas as pd

#app = Flask(__name__)

# Data reading
movie_dataset = pd.read_csv(r'testset_movies.csv')
array = np.load(r'test_emb.npy')

movies = movie_dataset['movieId'].to_list()
titles = movie_dataset['title'].to_list()
# drop the last part of title with the year: "(2005)"
titles_clipped = [" ".join(t.split(" ")[:-1]).lower() for t in titles]

'''
for i in range(len(movies)):
    response = google_images_download.googleimagesdownload()   #class instantiation
    m_id = movies[i]
    m_title = titles[i]
    k = m_title + " poster"

    arguments = {"keywords":k,"limit":2,"print_urls":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    print(paths)   #printing absolute paths of the downloaded images
'''




def get_soup(url,header):
    #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
    # 'html.parser')
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

for i in range(len(movies)):
    response = google_images_download.googleimagesdownload()   #class instantiation
    m_id = movies[i]
    m_title = titles[i]
    m_title = m_title.replace("/","").replace("&","and").replace("(","").replace(")","")
    k = m_title + " movie poster"
    query = k

    #query = sys.argv[1]

    query= query.split()
    query='+'.join(query)
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    #add the directory for your image here
    DIR="movie_posters"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)

    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("a",{"class":"iusc"}):
        #print a
        #mad = json.loads(a["mad"])
        #turl = mad["turl"]
        m = json.loads(a["m"])
        murl = m["murl"]
        turl = m["turl"]


        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        print(image_name)

        ActualImages.append((image_name, turl, murl))

    print("there are total" , len(ActualImages),"images")

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    #DIR = os.path.join(DIR, str(m_id))
    #if not os.path.exists(DIR):
    #    os.mkdir(DIR)

    ##print images
    for i, (image_name, turl, murl) in enumerate(ActualImages):
        if i > 1:
            break
        try:
            #req = urllib2.Request(turl, headers={'User-Agent' : header})
            #raw_img = urllib2.urlopen(req).read()
            #req = urllib.request.Request(turl, headers={'User-Agent' : header})
            raw_img = urllib.request.urlopen(turl).read()

            cntr = len([i for i in os.listdir(DIR) if image_name in i]) + 1
            #print cntr

            filename = str(m_id) + '.jpg'
            f = open(os.path.join(DIR, filename), 'wb')

            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : " + image_name)
            print(e)

        #break