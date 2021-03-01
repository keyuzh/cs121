# search.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

# Search and Retrieve
# • Once you have built the inverted index, you are ready to test document retrieval with
# queries.
# • At the very least, the documents retrieved should be returned based on tf-idf scoring. This
# can be done using
# • the cosine similarity method. Feel free to use a library to compute cosine similarity once you
# have the term frequencies and inverse document frequencies.
# • You may add other weighting/scoring mechanisms to help refine the search results

import pickle
import sys
import math
import itertools
from collections import defaultdict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QLineEdit,QPushButton,QLabel
from PyQt5.QtGui import QPixmap
#https://pypi.org/project/PyQt5/
#https://www.youtube.com/watch?v=Vde5SH8e1OQ&feature=emb_title


class Search:
    def __init__(self, index:dict, normalized_tf:dict, se):
        self.index = index
        self.normalized_tf = normalized_tf
        self.SearchEngine = se
        self.window = None
        self.logo = None
        self.textbox = None
        self.button = None

    #search return at most K urls where K = 20 in this case
    def search_url(self, keyword,K):
        '''out_list = []
        if keyword in self.index.keys():
            for l in self.index[keyword]:
                out_list.append((l[0], l[3]))

        out_list.sort(key=(lambda x: -x[1]))
        return out_list'''
        word_frequency = self.word_fq(keyword) # Get frequency of each word
        print("After tokenize query:")
        for word,fq in word_frequency.items():
            print (word,fq)
        word_frequency = self.normalize_tfidf(word_frequency) # get normalized value of each word
        print("After norm query;")
        for word,fq in word_frequency.items():
            print (word,fq)        
        doc_score = self.calculate_cosine_similarity(word_frequency) # return dict of doc with their score as value
        print("After cosine similarity: ")
        for doc, score in doc_score.items():
            print (doc,score)
        return sorted(doc_score.items(),key=lambda x:-x[1])[:K]
        # return dict(itertools.islice(doc_score.items(),K))

    # Return a dict() with
    # token = DocID, value = score
    def calculate_cosine_similarity(self,word_frequency):
        doc_score = defaultdict(int)
        for qword,qnorm in word_frequency.items():
            for did, doc in self.normalized_tf.items():
                if qword in doc.keys(): # word in the document
                    doc_score[did] += qnorm * doc[qword]
        return doc_score

        

    #Calculate tfidf and normalize
    def normalize_tfidf(self, word_frequency):
        #Courpus Count
        total_documents = len(self.normalized_tf)
        query_length = 0
        for word, freq in word_frequency.items():
            # print(self.index.keys())
            #if word in index -> calculate tfidf
            if word in self.index.keys():
                print("In index")
                df = len(self.index[word])
                word_frequency[word] = 1+math.log(freq,10) * math.log(total_documents/df,10)
                query_length += word_frequency[word]**2
            # else tfidf = 0
            else:
                print("Not in Index")
                word_frequency[word] = 0
        query_length = math.sqrt(query_length)
        for word, freq in word_frequency.items():
            if freq != 0:
                word_frequency[word] = freq / query_length
        return word_frequency
        
    #find word frequency in query
    def word_fq (self, word):
        query_token = word.split()
        query_dict = dict()
        for w in query_token:
            if w not in query_dict:
                query_dict[w] = 1
            else:
                query_dict[w] += 1
        return query_dict

    def search_length(self,keyword):
        if keyword in self.index.keys():
            return len(self.index[keyword])

    def search_button_clicked(self, textbox):
        print("Seaching...")
        print(self.textbox.text())
        #return a list of urls
        urls = self.search_url(self.textbox.text(),20)
        print("Finished.\nResult:")
        for doc, score in urls:
            print(doc,score)
        """
        window = QMainWindow()
        window.setGeometry(200,200,1000,1000)
        window.setWindowTitle("CS 121 Search Engine")
        window.setStyleSheet("background-color: white;")
        window.setFixedSize(1000, 1000)
        """
        pass

    def home_page(self):
        #Initialize the window
        self.window = QMainWindow()
        self.window.setGeometry(200,200,1000,1000)
        self.window.setWindowTitle("CS 121 Search Engine")
        self.window.setStyleSheet("background-color: white;")
        self.window.setFixedSize(1000, 1000)
        #Setup the Logo
        load_logo = QPixmap('guiLogo.png')
        self.logo = QLabel(self.window)
        self.logo.setPixmap(load_logo)
        self.logo.resize(load_logo.width(),load_logo.height())
        self.logo.move(200,200)
        #For textbox input
        self.textbox = QLineEdit(self.window)
        self.textbox.move(250,500)
        self.textbox.resize(500,40)
        #Create Search button
        self.button = QPushButton("Search",self.window)
        self.button.clicked.connect(self.search_button_clicked)
        self.button.move(450,550)
        #Display window
        self.window.show()
        sys.exit(self.SearchEngine.exec_())


if __name__ == '__main__':
    """
    inverted_index = pickle.load(open("inverted_index","rb"))
    search = Search(inverted_index)
    while True:
        keyword = input("Keyword:")
        if(keyword == "quit"):
            break
        urls = search.search_url(keyword)
        length = search.search_length(keyword)
        print("Length:", length)
        print("Url:")
        for url in urls[:20]:
            print(url[0])
    """
    se = QApplication(sys.argv)
    inverted_index = pickle.load(open("inverted_index","rb"))
    normalized_tf = pickle.load(open("normalized_tf","rb"))
    search = Search(inverted_index,normalized_tf, se)
    search.home_page()




