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
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QLineEdit,QPushButton
#https://pypi.org/project/PyQt5/
#https://www.youtube.com/watch?v=Vde5SH8e1OQ&feature=emb_title


class Search:
    def __init__(self, index:dict):
        self.index = index

    def search_url(self, keyword):
        if keyword in self.index.keys():
            out_list = []
            for l in self.index[keyword]:
                out_list.append(l[0])
            return out_list

    def search_length(self,keyword):
        if keyword in self.index.keys():
            return len(self.index[keyword])

def search_button_clicked():
    pass


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
            print(url)
    """
    SearchEngine = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(200,200,1000,1000)
    window.setWindowTitle("CS 121 Search Engine")
    textbox = QLineEdit(window)
    textbox.move(250,500)
    textbox.resize(500,40)
    button = QPushButton("Search",window)
    button.move(450,550)
    window.show()
    sys.exit(SearchEngine.exec_())




