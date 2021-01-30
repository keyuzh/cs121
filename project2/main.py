# main.py
# CS121 Winter 2021 Project 2: Web Crawler
# Group: 2
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1
import atexit
import logging

import sys

from corpus import Corpus
from crawler import Crawler
from frontier import Frontier
from analytics import Analytics

if __name__ == "__main__":
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # Instantiates frontier and loads the last state if exists
    frontier = Frontier()
    frontier.load_frontier()

    # Instantiates corpus object with the given cmd arg
    corpus = Corpus(sys.argv[1])

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    atexit.register(frontier.save_frontier)

    # Instantiates a crawler object and starts crawling
    analytics = Analytics()
    # register our analytics function
    atexit.register(analytics.write_all)
    crawler = Crawler(frontier, corpus, analytics)
    crawler.start_crawling()
