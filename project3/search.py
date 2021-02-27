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
from PyQt5.QtWidgets import QApplication, QMainWindow,QLineEdit,QPushButton,QLabel
from PyQt5.QtGui import QPixmap
#https://pypi.org/project/PyQt5/
#https://www.youtube.com/watch?v=Vde5SH8e1OQ&feature=emb_title


class Search:
    def __init__(self, index:dict):
        self.index = index

    def search_url(self, keyword):
        out_list = []
        if keyword in self.index.keys():
            for l in self.index[keyword]:
                out_list.append((l[0], l[3]))

        out_list.sort(key=(lambda x: -x[1]))
        return out_list

    def search_length(self,keyword):
        if keyword in self.index.keys():
            return len(self.index[keyword])

def search_button_clicked(textbox):
    print("button clicked")
    print(textbox.text())
    """
    window = QMainWindow()
    window.setGeometry(200,200,1000,1000)
    window.setWindowTitle("CS 121 Search Engine")
    window.setStyleSheet("background-color: white;")
    window.setFixedSize(1000, 1000)
    """
    pass

def home_page(SearchEngine):
    #Initialize the window
    window = QMainWindow()
    window.setGeometry(200,200,1000,1000)
    window.setWindowTitle("CS 121 Search Engine")
    window.setStyleSheet("background-color: white;")
    window.setFixedSize(1000, 1000)
    #Setup the Logo
    load_logo = QPixmap('guiLogo.png')
    logo = QLabel(window)
    logo.setPixmap(load_logo)
    logo.resize(load_logo.width(),load_logo.height())
    logo.move(200,200)
    #For textbox input
    textbox = QLineEdit(window)
    textbox.move(250,500)
    textbox.resize(500,40)
    #Create Search button
    button = QPushButton("Search",window)
    button.clicked.connect(search_button_clicked)
    button.move(450,550)
    #Display window
    window.show()
    sys.exit(SearchEngine.exec_())


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
    SearchEngine = QApplication(sys.argv)
    home_page(SearchEngine)




