# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:09:16 2021

@author: caleb
"""
import re
import multiprocessing
import urllib.request
from urllib.request import urlopen
import spacy
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
import pickle
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()  
class callback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.epoch = 0
        self.loss_to_be_subed = 0

    def on_epoch_end(self, model):
        loss = w2v_model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subed
        self.loss_to_be_subed = loss
        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.epoch += 1

filename1 = "W2VAbs_2.pickle"
classifier1= open(filename1, "rb")
w2v_model = pickle.load(classifier1)
classifier1.close()

stopWords = set(stopwords.words('english')) 

def w2v(keywords, negatives):
    keywords = re.sub("[^A-Za-z-_,']+", ' ', str(keywords))
    keyword = keywords.lower().split(",")
    key = [lemmatizer.lemmatize(x).replace("'","") for x in keyword if x not in stopWords]
    negative = re.sub("[^A-Za-z-_,']+", ' ', str(negatives))
    neg = negative.lower().split(",")
    ne = [lemmatizer.lemmatize(x).replace("'","") for x in neg if x not in stopWords]
    print(key,ne)
    k = [x for x in key if x in w2v_model.wv.vocab]
    n  = [x for x in ne if x in w2v_model.wv.vocab]    
    output = w2v_model.wv.most_similar(positive=k,negative =n, topn=5)
   

    return output

from flask import Flask, render_template, request
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
import time
from waitress import serve
app = Flask(__name__)

@app.route('/')
def student():
    return render_template('form.html')

@app.route('/',methods = ['POST','GET'])
def result():
    
    if request.method == 'POST':
        pos = request.form['presult']
        neg = request.form['nresult']
        print(pos,neg)
        results = w2v(pos,neg)
        returntext = "Results: <br>"
        for s,w in results:
            returntext = str(returntext)+ str(s.replace("_"," ")) + ":" + str(round(w,4)) + "<br>"
        html = open("C://Users/user/Documents/w2v/templates/form.html", encoding='utf-8').read().splitlines()
        
           
        html[2649] = returntext
        
        formname = os.listdir("C://Users/user/Documents/w2v/templates/")
        
        filenums = [x.replace("form","").replace(".html","") for x in formname]
        print(filenums)
        maxnum= len(filenums)-1
        if maxnum =="":
            maxnum =0 
        print(maxnum)
        num = int(maxnum) + 1
        filename = "form" + str(num) +".html"
        print(filename)
        fileloc = "C://Users/user/Documents/w2v/templates/"+str(filename)
        print(returntext)
        
        with open(fileloc, 'w',encoding='utf-8') as f:
            for item in html:
                f.write('%s\n' %item)
        os.stat("C://Users/user/Documents/w2v/templates/")
        time.sleep(0.5)
        return render_template(filename);

if __name__ == '__main__':
    
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port = "8080")

