import os
import pickle
import sys
import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QLineEdit,QPushButton,QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
#https://pypi.org/project/PyQt5/
#https://www.youtube.com/watch?v=Vde5SH8e1OQ&feature=emb_title
from corpus import Corpus
from project3.search import Search


class ResultWindow(QWidget):
    # https://www.learnpyqt.com/tutorials/creating-multiple-windows/
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self, query, result, corpus_path):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setWindowTitle(f"Results for {query}")
        self.setLayout(self.layout)
        self.result = result
        self.path = os.path.abspath(corpus_path)
        self.corpus = Corpus(corpus_path)

    def show(self) -> None:
        def wrapper(url):
            def open_in_webbrowser():
                webbrowser.open(url)
            return open_in_webbrowser

        for path in self.result:
            test = QLabel()
            local_link = os.path.join(self.path, path)
            print(local_link)
            button = QPushButton(self.corpus.get_title(path), self)
            button.clicked.connect(wrapper(local_link))
            url = self.corpus.get_url(path)
            test.setText(f"<a href=\"http://{url}\">{url}</a>")
            test.setOpenExternalLinks(True)
            self.layout.addWidget(button)
            self.layout.addWidget(test)
            self.layout.addSpacing(10)

        super().show()

class LoadingWindow(QWidget):
    def __init__(self, message: str):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setWindowTitle(message)
        self.setFixedSize(500, 1)
        self.show()

class MainWindow:
    def __init__(self, qapp):
        self.app = qapp
        self.search = None
        self.window = None
        self.logo = None
        self.textbox = None
        self.button = None
        self.result_window = None

    def search_button_clicked(self):
        query = self.textbox.text()
        #return a list of urls
        urls = self.search.search_url(query, 20)
        # for doc, score in urls:
        #     print(self.corpus.get_url(doc), score)
        #     print("Title:", self.corpus.get_title(doc), sep=' ')
        self.result_window = ResultWindow(query, [i[0] for i in urls], sys.argv[1])
        self.result_window.show()

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
        # self.button.setEnabled(False)
        #Display window
        self.window.show()
        sys.exit(self.app.exec_())

    def ready(self, search_engine):
        self.search = search_engine
        self.home_page()


if __name__ == '__main__':
    main_window = MainWindow(QApplication(sys.argv))
    loading_window = LoadingWindow("Loading inverted index")
    inverted_index = pickle.load(open("data/inverted_index","rb"))
    normalized_tf = pickle.load(open("data/normalized_tf","rb"))
    loading_window.close()

    search = Search(inverted_index, normalized_tf, sys.argv[1])
    main_window.ready(search)
