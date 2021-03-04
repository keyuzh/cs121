# gui.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

"""functions to render GUI"""

import os
import sys
import time
import webbrowser

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QWidget, QVBoxLayout

from corpus import Corpus


class ResultWindow(QWidget):
    # https://www.learnpyqt.com/tutorials/creating-multiple-windows/
    """Window for showing the results"""
    def __init__(self, corpus_path, query, result, result_count, runtime):
        super().__init__()
        self.result = result
        self.query = query
        self.result_count = result_count
        self.runtime = runtime
        self.path = os.path.abspath(corpus_path)
        self.corpus = Corpus(corpus_path)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle(f"{query} - CS121 Search")
        self.setBaseSize(500, 1000)

    def show(self) -> None:
        """overload the parent method to add results to the window"""
        def wrapper(url):
            # need a function object to register
            return lambda: webbrowser.open(url)
        # first line: show basic info about the search
        results = QLabel()
        results.setText(f"{self.query}: {self.result_count} results ({self.runtime:.4f} seconds)\n" +
                        f"Showing top {min(20, self.result_count)} results")
        self.layout.addWidget(results)
        self.layout.addSpacing(10)
        # if not found
        if self.result_count == 0:
            empty_results = QLabel()
            empty_results.setText("No Results found. Did you enter a stop word or make a typo?")
            self.layout.addWidget(empty_results)
            self.layout.addSpacing(10)
        # display results
        for path in self.result:
            link = QLabel()
            local_link = os.path.join(self.path, path)
            # button to local file
            button = QPushButton(self.corpus.get_title(path), self)
            button.clicked.connect(wrapper(local_link))
            # link to internet site
            url = self.corpus.get_url(path)
            link.setText(f"<a href=\"http://{url}\">{url[:100]}</a>")
            link.setOpenExternalLinks(True)
            self.layout.addWidget(button)
            self.layout.addWidget(link)
        # call parent method
        super().show()


class LoadingWindow(QWidget):
    """window to show when loading the index"""
    def __init__(self, message: str):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setWindowTitle(message)
        self.setFixedSize(500, 1)
        self.show()


class MainWindow:
    """main search window"""
    def __init__(self, qapp, corpus):
        # initialize variables
        self.app = qapp
        self.corpus_path = corpus
        self.search = None
        self.window = None
        self.logo = None
        self.textbox = None
        self.button = None
        self.result_window = None

    def search_button_clicked(self):
        """get the query from text box and perform a search"""
        query = self.textbox.text().lower()
        # time the search
        start = time.time()
        num_results, urls = self.search.search(query, 20)
        search_time = time.time() - start
        # render the result window
        self.result_window = ResultWindow(self.corpus_path, query, [i[0] for i in urls], num_results, search_time)
        self.result_window.show()

    def home_page(self):
        # Initialize the window
        self.window = QMainWindow()
        self.window.setGeometry(200, 200, 1000, 1000)
        self.window.setWindowTitle("CS 121 Search Engine")
        self.window.setStyleSheet("background-color: white;")
        self.window.setFixedSize(1000, 1000)
        # Setup the Logo
        load_logo = QPixmap('guiLogo.png')
        self.logo = QLabel(self.window)
        self.logo.setPixmap(load_logo)
        self.logo.resize(load_logo.width(), load_logo.height())
        self.logo.move(200, 200)
        # For textbox input
        self.textbox = QLineEdit(self.window)
        self.textbox.move(250, 500)
        self.textbox.resize(500, 40)
        # Create Search button
        self.button = QPushButton("Search", self.window)
        self.button.clicked.connect(self.search_button_clicked)
        self.button.move(450, 550)
        # Display window
        self.window.show()
        sys.exit(self.app.exec_())

    def ready(self, search_engine):
        """ready to render"""
        self.search = search_engine
        self.home_page()
