import re
import nltk
from nltk import word_tokenize
from nltk import ngrams
from collections import Counter, OrderedDict
from collections import defaultdict
import string
import sys

import pandas as p

def v1(postrain,postest):
    Posdata = []
    Posdatatest =  []
    finaltestdata = []
    finaltestdatatags = []
    finaltestdatawords = []
    
    
    Posdata = postrain.read()
    postrain.close()
    
    Posdatatest = postest.read()
    postest.close()
    
    testdata = Posdatatest.split(' ')
    
    
    for i in range(0,len(testdata)):
        
           #testdata[i] = testdata[i].remove('\n')
        if '/' in testdata[i]:
            finaltestdata= testdata[i].split('/')
            finaltestdatatags.append(finaltestdata[1])
            finaltestdatawords.append(finaltestdata[0])
                #finaltestdata.append(i.split('/')[0])
                #finaltestdatatagswords.append(i.split('/')[1])
        #finaltestdatatags = finaltestdata[1]
        #finaltestdatatags= finaltestdata[1]
        #finaltestdatatagswords = finaltestdata[0]
    

    newdata = ''

    #splitting traindata into sentence
    Sentences = Posdata.splitlines()
    for sentence in Sentences:
        sentence= 'φ'+sentence
        newdata = newdata + sentence
        
    #total sentences in traindata
    
    sentenceCount = len(Sentences)

    wordTagTokens = nltk.word_tokenize(newdata)
    firstTags = []
    firstWords = []
    wordTokens = []
    tagTokens =[]
    wordTagCounter = dict()
    wordCounter = dict()
    tagCounter = dict()
    for wordTag in wordTagTokens:
        if '/' in wordTag:
            wordAndTag = wordTag.split('/')
            if wordAndTag[1].isalpha():
                if 'φ' in wordAndTag[0]:
                    wordAndTag[0] = wordAndTag[0][1:] #remove 'φ'
                    wordTag = wordTag[1:]
                    firstTags.append(wordAndTag[1])
                    firstWords.append(wordAndTag[0])
                wordTokens.append(wordAndTag[0])
                tagTokens.append(wordAndTag[1])

                if wordAndTag[0] in wordCounter:
                    wordCounter[wordAndTag[0]] = wordCounter[wordAndTag[0]] +1
                else:
                    wordCounter[wordAndTag[0]] =1
                if wordTag in wordTagCounter:
                    wordTagCounter[wordTag] = wordTagCounter[wordTag] +1
                else:
                    wordTagCounter[wordTag] =1
                if wordAndTag[1] in tagCounter:
                    tagCounter[wordAndTag[1]] = tagCounter[wordAndTag[1]] +1
                else:
                    tagCounter[wordAndTag[1]] =1


    bigramWords = nltk.bigrams(wordTokens)
    bigramWordsCounter = Counter(bigramWords)

    bigramTags = nltk.bigrams(tagTokens)
    bigramTagsCounter = Counter(bigramTags)

    totalTags = len(tagTokens)
    totalDisctinctTags = len(tagCounter)
    totalWords = len(wordTokens)
    
    Score = dict()
    BackPtr = dict()
    Seq = dict()
    count =0
    for sentence in Sentences:
        count = count +1        

        maxTagWord = dict()
        maxScore = 0
        sentenceWordTags = []
        sentenceWordTags = re.split(' ',sentence)
        #sentenceWordTags[0] = sentenceWordTags[0][1:] #remove 'φ' this was removed in previous step
        sentenceWords = []
        sentenceTags = []
        for taggedWord in sentenceWordTags:
            if '/' in taggedWord:                
                wordAndTag = taggedWord.split('/')
                if  wordAndTag[1].isalpha():
                    sentenceWords.append(wordAndTag[0])
                    sentenceTags.append(wordAndTag[1])
        #wordcount in a sentence        
        wordcountinsentence = len(sentenceWords)
        if wordcountinsentence == 0:
            continue
           
        for tag in tagCounter:
            Score[tag] = dict()
            BackPtr[tag] = dict()              
            
            if (sentenceWords[0]+'/'+tag)  in wordTagCounter:
                firstWordWithTagCount = wordTagCounter[sentenceWords[0]+'/'+tag]
                #re.findall(words[0]+'/'+tagTokens[t]+' ',newdata) #find all instances in wholedata of first word of this sentence occurs current tag
                probFirstWordWithTag = firstWordWithTagCount/totalTags #prob of first word of sentence with current tag
                #patternallTags = re.findall('φ '+r'\S+/'+allTags[t]+' ',newdata) # how many times this tag occurs as first tag of sentence
                firstTagCount = firstTags.count(tag)
                probTagFirstInSentence = firstTagCount/sentenceCount
                Score[tag][sentenceWords[0]] = probFirstWordWithTag* probTagFirstInSentence
            else:
                Score[tag][sentenceWords[0]] = 0
            if(Score[tag][sentenceWords[0]]>maxScore):
                maxScore = Score[tag][sentenceWords[0]]
                maxTagWord[sentenceWords[0]] = tag

            BackPtr[tag][sentenceWords[0]] = tag
            
        for w in range(1,wordcountinsentence):
            maxScore =0
            maxTagWord[sentenceWords[w]] = sentenceTags[w]
            for tag in tagCounter:
                maxVal=0
                maxIndex =tag
                if (sentenceWords[w]+'/'+tag) in wordTagCounter :
                    wordWithTagCount = wordTagCounter[sentenceWords[w]+'/'+tag]
                    #re.findall(sentenceWords[w]+'/'+tagTokens[t]+' ',newdata)
            #2nd pattern count in a traindata 
    #                pattern2count = len(pattern2) 
                    probWordWithTag =  wordWithTagCount/totalTags  

                    for jtag in tagCounter:
                        tTagFollowsjTag = bigramTagsCounter[(jtag,tag)]  
                        #re.findall(tagTokens[j]+r' \S+/'+tagTokens[t]+' ',newdata)
                        jTagCount = tagCounter[jtag]
                        probtTagFollowsjTag =  tTagFollowsjTag/jTagCount
                        value = Score[jtag][sentenceWords[w-1]] * probtTagFollowsjTag
                        if(value>maxVal):
                            maxVal = value
                            maxIndex = jtag
                    Score[tag][sentenceWords[w]] = probWordWithTag * maxVal
                else:
                    Score[tag][sentenceWords[w]] = 0    
                BackPtr[tag][sentenceWords[w]] =  maxIndex
                if Score[tag][sentenceWords[w]] > maxScore:
                    maxScore = Score[tag][sentenceWords[w]] 
                    maxTagWord[sentenceWords[w]] = tag
        
        Seq[sentenceWords[wordcountinsentence-1]] = maxTagWord[sentenceWords[wordcountinsentence-1]]
        for w in range(wordcountinsentence-2,-1,-1):
            Seq[sentenceWords[w]] = BackPtr[Seq[sentenceWords[w+1]]][sentenceWords[w+1]]

             
                   
         
    #print(Seq)
    finaltestdatawordTags = []
    trainedTags = []
    matchCount =0.0
    for i in range(0,len(finaltestdatawords)):
        word = finaltestdatawords[i] 
        if '\n' in word:
               word = word[1:]
        if word in Seq:
            finaltestdatawordTags.append(finaltestdatawords[i] + '/'+ Seq[word])
            if(finaltestdatatags[i]==Seq[word]):
                matchCount =matchCount +1
        else:
            finaltestdatawordTags.append(finaltestdatawords[i] + '/NN')
            if(finaltestdatatags[i]=='/NN'):
                matchCount = matchCount +1
    
    #print(finaltestdatawordTags)
    print('Accuracy is',(matchCount*100.0)/float(len(finaltestdatawords)))
    f = open('POS.test.out','a+')        
    f.write(' '.join(finaltestdatawordTags))
    f.close()

    
    

def main():
    
    input1 = sys.argv[1]
    input2 = sys.argv[2]
    trainfile = open(input1)
    testfile = open(input2)
    v1(trainfile,testfile)
    
    
        
if __name__ == "__main__":
    main()