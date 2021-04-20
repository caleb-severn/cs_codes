# -*- coding: utf-8 -*-

"""

Created on Wed Jul  3 09:50:49 2019

 

@author: csevern

"""

import nltk

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer

from nltk.tokenize import word_tokenize, sent_tokenize

import re

from nltk.stem import WordNetLemmatizer

import time

lemma = WordNetLemmatizer

ls = WordNetLemmatizer()



def _create_frequency_table(text_string) -> dict:

    """

    we create a dictionary for the word frequency table.

    For this, we should only use the words that are not part of the stopWords array.

    Removing stop words and making frequency table

    Stemmer - an algorithm to bring words to its root word.

    :rtype: dict

    """

    stopWords = set(stopwords.words("english"))

    text_string = re.sub('[^A-Za-z0-9_]+ ', ' ', text_string).replace(".", " ").replace(",", " ").replace("?", " ").replace("'", "").replace("\n", " ").replace("-", " ").replace("\\u", " ").replace("  ", " ")

 

    words = text_string.lower().split(" ")

    ps = PorterStemmer()

    ls = WordNetLemmatizer()

 

    freqTable = dict()

    freqTable2 = dict()

    for word in words:

        #word = ps.stem(word)

 

        if word in stopWords:

 

            continue

        word = ls.lemmatize(word)

        word2 = ps.stem(word)

        if word == "":

            continue

       

        if word in freqTable:

            freqTable[word] += 1

        else:

            freqTable[word] = 1

        if word2 in freqTable2:

            freqTable2[word2] +=1

        else:

            freqTable2[word2] =1

   

    return freqTable, freqTable2

 

 

def _score_sentences(sentences, freqTable, freqTable2) -> dict:

    """

    score a sentence by its words

    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.

    :rtype: dict

    """

 

    sentenceValue = dict()

    ps = PorterStemmer()

    ls = WordNetLemmatizer()

    #ps=ls

    #print(len(sentences))

 

    for i in range(0,len(sentences)):

       

        sentence = sentences[i]

        #print(sentence, i, len(sentences))

       

        if i == 0 or i == len(sentences)-1:

            weight = 0.2*(len(word_tokenize(sentence)))

        else:

            weight = 0

       

        propnoun =0

        sentenceoriginal = sentence

        sentwords = word_tokenize(sentence)

        sentwords[0] = sentwords[0].lower()

        postags = nltk.pos_tag(sentwords)

        for k,v in postags:

            if v == "NNP" or v == "NNPS":

                propnoun +=1

            if (v == "PRP") and '"' in sentence:

                if i >= 1:

                    postags2 = nltk.pos_tag(word_tokenize(sentences[i-1]))

                    if ("NNP" not in str(postags)) and "NNPS" not in str(postags) and "NNP" not in str(postags2) and "NNPS" not in str(postags2):

                        weight = -1*len(word_tokenize(sentence))

                else:

                    if ("NNP" not in str(postags)) and "NNPS" not in str(postags):

                        weight = -1*len(word_tokenize(sentence))                   

        sentence =  re.sub('[^A-Za-z0-9_]+ ', ' ', sentence.lower()).replace(".", " ").replace(",", " ").replace("?", " ").replace("'", "").replace("\n", " ").replace("-", " ").replace("\\u", " ").replace("  ", " ")

        #sentence = ' '.join(ps.stem(word) for word in word_tokenize(sentence))

        sentence1 = ' '.join(ls.lemmatize(word) for word in word_tokenize(sentence))

        sentsplit1 = sentence1.split(" ")

        #sentence2 = ' '.join(ps.stem(word) for word in word_tokenize(sentence))

        #sentsplit2 = sentence2.split(" ")

        #word_count_in_sentence = (len(word_tokenize(sentence)))

        word_count_in_sentence_except_stop_words = 0

        for wordValue in freqTable:

            if wordValue in sentsplit1:

 

                word_count_in_sentence_except_stop_words += 1

                if sentenceoriginal[:10] in sentenceValue:

                    sentenceValue[sentenceoriginal[:10]] += freqTable[wordValue]

                else:

                    sentenceValue[sentenceoriginal[:10]] = freqTable[wordValue]

 

        if sentenceoriginal[:10] in sentenceValue:

            #print(sentenceoriginal, sentenceValue[sentenceoriginal[:10]] / word_count_in_sentence_except_stop_words, sentenceValue[sentenceoriginal[:10]], word_count_in_sentence_except_stop_words )

            #print(sentenceoriginal, propnoun)

            #print(postags)

            sentenceValue[sentenceoriginal[:10]] = ((sentenceValue[sentenceoriginal[:10]]+propnoun+weight) / word_count_in_sentence_except_stop_words)

            #print(sentenceoriginal, sentenceValue[sentenceoriginal[:10]] , propnoun, weight, word_count_in_sentence_except_stop_words)

   

    return sentenceValue

 

 

def _find_average_score(sentenceValue) -> int:

    """

    Find the average score from the sentence value dictionary

    :rtype: int

    """

    sumValues = 0

    for entry in sentenceValue:

        sumValues += sentenceValue[entry]

 

    # Average value of a sentence from original text

    average = (sumValues / len(sentenceValue))

 

    return average

 

 

def _generate_summary(sentences, sentenceValue, threshold):

    sentence_count = 0

    summary = ''

 

    for sentence in sentences:

        #print(sentence)

        #print(sentence[:10])

        #print(len(sentenceValue))

        #if sentence[:10] in sentenceValue:

            #print(sentenceValue[sentence[:10]])

            #print(threshold)

        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):

            #print(sentenceValue[sentence[:10]])

            #print(threshold)

            summary += " " + sentence

            sentence_count += 1

 

    return summary

 

 

def run_summarization(text_str):

    dictionary = []

    # 1 Create the word frequency table

    freq_table, freq_table2 = _create_frequency_table(text_str)



    for k,v in freq_table.items():

        dictionary.append(k)

    #print(len(freq_table))

    '''

    We already have a sentence tokenizer, so we just need

    to run the sent_tokenize() method to create the array of sentences.

    '''

 

    # 2 Tokenize the sentences

    sentences = sent_tokenize(text_str)
    words = word_tokenize(text_str)
 

    # 3 Important Algorithm: score the sentences

    sentence_scores = _score_sentences(sentences, freq_table, freq_table2)

 

    # 4 Find the threshold

    threshold = _find_average_score(sentence_scores)

   

    factor = 0.3

    sumvalue = 1
    text_str = text_str
    if len(words) < 250:

        limit = 0.5

    elif len(words) > 1000:

        limit = 0.20

    elif len(words) > 10000:
        limit= 0.05
    else:
        limit = 0.33

 

    if len(dictionary) > 250:

        dictlimit = 0.20

    else:

        dictlimit = 0.33

    dictper =0

    diff = 1.0

    r=0

    while diff > limit and r <50:

        r+=1

        sentsorted = {k: v for k, v in sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)}

        i=0

        for k, v in sentsorted.items():

            i+=1

            value = v

            if i == int(len(sentences)*factor):

                threshold = value

        #print(threshold, factor)

 

   

            #if i == int(len(sentences/4)):

               

            

        

        # 5 Important Algorithm: Generate the summary

        #value = (threshold + float(max(sentence_scores)))/2

        #print(value*threshold, threshold,float(max(sentence_scores)))

        #value = 1.0

   

        dictcount = 0

        summary = _generate_summary(sentences, sentence_scores, threshold)

        sumvalue = len(word_tokenize(summary))/len(word_tokenize(text_str))


        sumsentences = sent_tokenize(summary)
        sumwords = (' '.join(ls.lemmatize(word) for word in word_tokenize(summary))).split(" ")

        for d in dictionary:

            if d in sumwords:

                dictcount +=1

        dictper = dictcount/len(dictionary)



        if dictper < dictlimit and sumvalue<limit:

            factor +=0.01

        else:

            factor -=0.01

        diff= abs(dictper - dictlimit) + abs(sumvalue-limit)

        #print("This much different:", diff)
    summary = re.sub("[^0-9a-zA-Z,'.-]+ ", ' ', summary)
    summary = summary.replace(" , "," ")
    summarysent = sent_tokenize(summary)
    if len(summarysent)>10:
        summary = ' '.join(summarysent[:10])
    else:
        summary = ' '.join(summarysent)

    return summary

 

 
   #result = run_summarization(text_str)

    #print(result)


