# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 08:43:55 2020

@author: caleb
"""

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import re
import pandas as pd
import numpy as np
import time
from PIL import Image
from io import BytesIO
import nltk
from bs4 import BeautifulSoup, NavigableString, Tag
import summerizer as sr
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def gettop(sites,country,papers):
    final_links = []
    for x, url in enumerate(sites):
        try:
            r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html_page  = urlopen(r)
    
            soup = bs(html_page, "html.parser")
            imagewidth = []
            imageheight = []
            links = []   
            imglink = []
            re_link = ""
            fail=0
            mainlist = soup.find('main')
            if mainlist != None:
                articles = mainlist.findAll('a')
            else:
                articles = soup.findAll('a')
                
                
            for i,link in enumerate(articles):
                children = link.findChildren("source")
                if len(children) == 0:
                    children = link.findChildren("img")
                newslink = link.get('href')
                
        
                for i, img in enumerate(children):
                    if img == "":
                        continue
                    try:
        
                        if newslink == url or newslink == url[:-1] or str(newslink)[-4:] == "com/" or "resources" in str(newslink) or "sport" in str(newslink) or len(newslink) <10 or "facebook" in newslink:
                            continue
            
                        if img.has_attr('width') and ("%" not in img['width']):
                            try:
                                width = float(img['width'].strip("%").strip("px").strip("em"))
                            except:
                                width = 0
                            if img.has_attr('height'):
                                try:
                                    height = float(img['height'].strip("%").strip("px").strip("em"))
                                except:
                                    height = 0.5*width
                            else:
                                height = 0.5*width
                            imagewidth.append(round(width,-1))
                            imageheight.append(round(height,-1))   
                            links.append(newslink)                    
                        else:
                            size = img.get('srcset')
                            
                            if size == None:
                                size =img.get('data-srcset')
                            if size == None:
                                size =img.get('src')
                            
                            if "w" in size[-4:]:
                                size = size[-4:].strip("w")
                                
                            if "," in str(size):
                                sizesplit = size.split(",")
                                size = sizesplit[len(sizesplit)-1]
                            
                            if " " in str(size):
                                sizesplit = size.split(" ")
                                size = sizesplit[0]
                                if "width" in size:
                                    size = sizesplit[1].strip("w").strip("px")
                                if size == "":
                                    size = sizesplit[1]
            
                            size = str(size).strip("'")
              
                            if size == "":
                                continue
                            if "https:" not in size and size.isdigit() == False:
                                try:
                                    size = "https:" + size
            
                                    r = Request(size, headers={'User-Agent': 'Mozilla/5.0'})     
                
                                    im=Image.open(urlopen(r))
                                    width, height = im.size
              
                                    imagewidth.append(round(width,-1))
                                    imageheight.append(round(height,-1))
                                    links.append(newslink)
                                except:
            
                                    size = url + size.strip("https:")
            
                                    r = Request(size, headers={'User-Agent': 'Mozilla/5.0'})    
                
                                    im=Image.open(urlopen(r))
                                    
                                    width, height = im.size
                                    #num = re.sub("[^0-9.]", "",size)
                     
                                    imagewidth.append(round(width,-1))
                                    imageheight.append(round(height,-1))
                                    links.append(newslink)
                            else:
                                if size.isdigit() == True:
            
                                    imagewidth.append(round(float(size),-1))
                                    imageheight.append(round(0.5*float(size),-1))
                                    links.append(newslink)  
                                else:
                                    r = Request(size, headers={'User-Agent': 'Mozilla/5.0'})    
                    
                                    im=Image.open(urlopen(r))
                                    
                                    width, height = im.size
                                    #num = re.sub("[^0-9.]", "",size)
                
                                    imagewidth.append(round(width,-1))
                                    imageheight.append(round(height,-1))
                                    links.append(newslink)
                    except:
                        fail+=1
        
            if len(imagewidth) == 0:
                for i,link in enumerate(soup.findAll('main')):
                    children = link.findChildren("a")
                    if len(children)==0:
                        for i,link2 in enumerate(soup.findAll('main')):
                            newslink = link2.get('href')
                            if i > 12 and "http" in str(newslink) and newslink != None and str(newslink)[-2:].isdigit() == True:
                                re_link = newslink
                                break
                    else:                    
                        for i, link2 in enumerate(children):
                            
                            newslink = link2.get('href')
                            if newslink != None and str(newslink)[-2:].isdigit() == True:
                                re_link = newslink
                                break
        
                    
            img_link = pd.DataFrame(list(zip(links, imagewidth, imageheight)), columns=["links","imgs-w", "imgs-h"])
            img_link["imgs-w"] = pd.to_numeric(img_link["imgs-w"], downcast = "float")
            img_link["imgs-h"] = pd.to_numeric(img_link["imgs-h"], downcast = "float")    
            if "https://www.reuters.com/news/archive" not in url:
                img_link2= img_link[(img_link["imgs-w"] >= 100.0) & (img_link["imgs-h"] >= 100.0) & (img_link["links"].str.contains("video")==False)]
            else:
                img_link2 = img_link[img_link["links"].str.contains("video")==False]
            if "allafrica" in url or "https://www.reuters.com/news/archive" in url or "http://jamaica-gleaner":
                sorteddf =img_link2.rename_axis('MyIdx').sort_values(by = ['MyIdx','imgs-w'], ascending = [True,False])
            else:
                sorteddf =img_link2.rename_axis('MyIdx').sort_values(by = ['imgs-w','MyIdx'], ascending = [False,True])             
            if re_link == "":
                re_link = sorteddf.iloc[0,0]
                if "banner" in re_link:
                    re_link = sorteddf.iloc[1,0]
            if "euronews" in url:
                re_link = "https://www.euronews.com/" + re_link
            if "reuters" in url and "ca.reuters" not in url:
                re_link = "https://www.reuters.com/" + re_link
            if "allafrica" in url:
                re_link = "https://allafrica.com/" + re_link
            if "aljazeera.com" in url:
                re_link = "https://www.aljazeera.com" + re_link
            if "http" not in re_link and "bbc" not in str(url):
                re_link = url + re_link
            elif "http" not in re_link and "bbc" in str(url):
                re_link = "https://bbc.co.uk" + re_link
            #print(url, re_link)
            final_links.append(re_link)
        except:
            final_links.append("")
    return final_links;






def getarticle(fdf):
    articlelist = fdf["Top"].tolist()
    articles = []
    for i, a in enumerate(articlelist):

        try:
            a = a.encode('cp1252')
            r = Request(a.decode('cp1252'), headers={'User-Agent': 'Mozilla/5.0'})    
            html_page  = urlopen(r)
            soup = bs(html_page, "html.parser")
            try:
                title = soup.find('h1').get_text()
            except:
                title =""
            newtext = []
            for p, text in enumerate(soup.findAll('p')):
                
                for tag in text:
                    if isinstance(tag, NavigableString):
                        newtext.append(tag)
                    else:
                        clean = tag.get_text()
                        
                        if "css" not in clean:
                            newtext.append(clean)
            cleanedtext = ' '.join(newtext).replace('"',"'").replace(" .",".")
            cleanedtext = re.sub("[^a-zA-Z0-9.,' ]", "",cleanedtext)
            title = re.sub("[^a-zA-Z0-9.,' ]", "",title)
            cleanedtext = title + ". " + cleanedtext
            cleanedtext = cleanedtext.replace("InFocus","").replace("Read More","").replace("Watch Euronews live stream","").replace("Share this article",".")
            sentences = nltk.sent_tokenize(cleanedtext)
            safe_sent = []
            for s in sentences:
                if "@" not in s and "http" not in s and "Reporting by" not in s and "©" not in s and "Share this" not in s and "Reuters" not in s:
                    safe_sent.append(s)
            cleanedtext = ' '.join(safe_sent)
    
            sentlen = len(nltk.sent_tokenize(cleanedtext))
            if sentlen > 10:
                transtitle = cleanedtext.split(".")[0]
                result = sr.run_summarization(str(cleanedtext))
            else:
                result = cleanedtext
                transtitle = cleanedtext.split(".")[0]
            if transtitle[:int((0.7*len(transtitle)))] not in str(result):
                result = transtitle + ". " + result
            articles.append(result)

        except:
            print("failed")
            articles.append(" ")
    fdf["Articles"] = pd.Series(articles)
    return fdf

def generatehtml(newdf,sid,Codes,Countries):
    print("writing articles")
    html = open("C://Users/user/Documents/Website/projects.html").readlines()
    print("File Opened")
    mCountry = newdf['Country'].tolist()
    mArticle = newdf['Articles'].tolist()
    linelist = []

    for i, cont in enumerate(mCountry):
        print(cont)
        try:
            sents = nltk.sent_tokenize(str(mArticle[i]))
            
            sentArt = [x.replace("\n","").replace("READ MORE","").replace("InFocus","").replace("Read More","") for x in sents[:8] if (("advertising" not in str(x)) or ("Copywrite" not in str(x)) or ("Avertisement" not in str(x)) or ("http" not in str(x)) or ("@" not in str(x)) or ("all rights reserved" not in str(x).lower()))]
            
            scores = []
            for sent in sentArt:
                ss = sid.polarity_scores(sent)
                value = ss['compound']
                scores.append(float(value))
            score = np.mean(scores)
            if str(score) == "nan":
                score = 0
            newarticle ='. '.join(sentArt)
            #texts = nltk.word_tokenize(newarticle)
            r=1
            newswords = nltk.word_tokenize(newarticle)
            newarticle1 = ""
            y=0
            for x in range(0,len(newswords)+1):
                if x > r*7:
                    letters = str(' '.join(newswords[y:x]))   
                    if len(letters) > 50:        
                        newarticle1 = newarticle1 + "\\r\\n" + str(' '.join(newswords[y:x]))
                    else:
                        
                        x+=1
                        letters =  str(' '.join(newswords[y:x]))
                        if len(letters) < 50:
                            x+=1   
                            newarticle1 = newarticle1 + "\\r\\n" + str(' '.join(newswords[y:x]))
                        else:
                            newarticle1 = newarticle1 + "\\r\\n" + str(' '.join(newswords[y:x]))
                            
                    y=x
                    r+=1
            newarticle1 = "\\r\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t" + str(newarticle1)
            #combined = ' '.join(texts)
            combined = newarticle1.replace("'","’").replace(" , ",", ").replace(" ’ ","’").replace("..",".")
            line = "\t\t[{v:'" + str(Codes[Countries.index(cont)]) +"',f:'" + str(cont).replace("'","") + "'},"+str(score)+",'"+str(combined)+"'],\n"
            linelist.append(line)
        except:
            print("couldnt do", cont)

    localtime = time.asctime( time.localtime(time.time()) )
    print("updated at:" ,localtime)
    printtime = '\t\t\t\t\t\t\t<i>Last Updated : '+ str(localtime) + '</i></p>\n'

    find2 = html.index('\t\t\t\t\t\t\t<i>Last Updated : [TIME]</i></p>\n')
    html[find2] = printtime
    find = html.index('\t\t\t\t\t\t\t\t[INSERT DATA HERE]\n')
    html[find:find] = linelist
    del html[html.index('\t\t\t\t\t\t\t\t[INSERT DATA HERE]\n')]
    
    
    savefile= "C://Users/user/Documents/GitHub/caleb-severn.github.io/world-news.html"
    with open(savefile, 'w', encoding='utf-8') as f:
        for item in html:
            f.write('%s' %item)
    savefile= "C://Users/user/Documents/GitHub/caleb-severn.github.io/projects.html"
    with open(savefile, 'w', encoding='utf-8') as f:
        for item in html:
            f.write('%s' %item)


def run_news():
    fdf = pd.read_csv("C://Users/user/Documents/Website/sites.csv", encoding='utf-8')
    sites = fdf["Website"].tolist()
    papers = fdf["Paper"].tolist()
    country = fdf["Country"].tolist()
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    final_links = gettop(sites,country,papers)
    fdf["Top"] = pd.Series(final_links)
    fdf.to_csv("C://Users/user/Documents/Website/sites_top.csv", encoding='utf-8')
    newdf = getarticle(fdf)
    newdf.to_csv("C://Users/user/Documents/Website/sites_article.csv", encoding='utf-8')
    iso = pd.read_csv("C://Users/user/Documents/Website/ISO.csv")
    Countries = iso["Country"].tolist()
    Codes = iso["Code"].tolist()
    

    sid = SentimentIntensityAnalyzer()

    generatehtml(newdf,sid,Codes,Countries)

    
    