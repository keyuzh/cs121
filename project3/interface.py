# interface.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

"""user interface to the search engine, CLI and GUI available"""

import getopt
import pickle
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from cli import CLI
from gui import *
from search import Search

DEFAULT_CORPUS_POSITION = "./WEBPAGES_RAW"
DEFAULT_INDEX_DIRECTORY = "./data"


def parse_arguments(args):
    """parse command line arguments"""
    corpus = DEFAULT_CORPUS_POSITION
    index = DEFAULT_INDEX_DIRECTORY
    bigram = False
    gui = False
    # https://www.geeksforgeeks.org/command-line-arguments-in-python/
    # Remove 1st argument (current file) from the list of command line arguments
    argument_list = args[1:]
    # Options
    options = "c:i:bg"
    # Long options
    long_options = ["corpus =", "index =", "bigram", "gui"]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argument_list, options, long_options)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        raise
    for arg, value in arguments:
        if arg in {"-c", "--corpus"}:
            corpus = value
        elif arg in {"-i", "--index"}:
            index = value
        elif arg in {"-b", "--bigram"}:
            bigram = True
        elif arg in {"-g", "--gui"}:
            gui = True
    return corpus, index, bigram, gui


def load_gui(index: str or Path, bigram: bool) -> Search:
    """load index files for gui and create the search object"""
    index = Path(index)
    load = LoadingWindow("Loading Inverted Index")
    inverted_index = pickle.load(open(index / "inverted_index", "rb"))
    load.close()
    load = LoadingWindow("Loading TFIDF Scores")
    normalized_tf = pickle.load(open(index / "normalized_tf", "rb"))
    load.close()
    if bigram:
        load = LoadingWindow("Loading Bigram Inverted Index")
        inverted_index_bi = pickle.load(open(index / "inverted_index_bigram", "rb"))
        load.close()
        load = LoadingWindow("Loading Bigram TFIDF Scores")
        normalized_tf_bi = pickle.load(open(index / "normalized_tf_bigram", "rb"))
        load.close()
    else:
        inverted_index_bi = None
        normalized_tf_bi = None
    load = LoadingWindow("Loading HTML Tag Information")
    html_tag = pickle.load(open(index / "html_tag", 'rb'))
    load.close()
    return Search(corpus, inverted_index, normalized_tf, html_tag, inverted_index_bi, normalized_tf_bi)


def load_cli(index: str or Path, bigram: bool) -> Search:
    """load index files and create the search object"""
    index = Path(index)
    print("Loading Inverted Index")
    inverted_index = pickle.load(open(index / "inverted_index", "rb"))
    print("Loading TFIDF Scores")
    normalized_tf = pickle.load(open(index / "normalized_tf", "rb"))
    if bigram:
        print("Loading Bigram Inverted Index")
        inverted_index_bi = pickle.load(open(index / "inverted_index_bigram", "rb"))
        print("Loading Bigram TFIDF Scores")
        normalized_tf_bi = pickle.load(open(index / "normalized_tf_bigram", "rb"))
    else:
        inverted_index_bi = None
        normalized_tf_bi = None
    print("Loading HTML Tag Information")
    html_tag = pickle.load(open(index / "html_tag", 'rb'))
    return Search(corpus, inverted_index, normalized_tf, html_tag, inverted_index_bi, normalized_tf_bi)


if __name__ == '__main__':
    corpus, index, bigram, gui = parse_arguments(sys.argv)
    if gui:
        main_window = MainWindow(QApplication(sys.argv), corpus)
        search = load_gui(index, bigram)
        main_window.ready(search)
    else:
        search = load_cli(index, bigram)
        cli = CLI(search, corpus)
        while True:
            print()
            query = input("Enter Query (type ':q' to exit): ")
            if query == ':q':
                break
            cli.start_search(query)
