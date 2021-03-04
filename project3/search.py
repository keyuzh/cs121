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
import os
import pickle
import sys
import math
import webbrowser
import itertools
from collections import defaultdict
from pathlib import Path

from corpus import Corpus


class Search():
    def __init__(self, index: dict, normalized_tf: dict, corpus_path: str or Path):
        self.corpus = Corpus(corpus_path)
        self.index = index
        self.normalized_tf = normalized_tf
        # self.SearchEngine = se


    # search return at most K urls where K = 20 in this case
    def search_url(self, keyword, K):
        '''out_list = []
        if keyword in self.index.keys():
            for l in self.index[keyword]:
                out_list.append((l[0], l[3]))

        out_list.sort(key=(lambda x: -x[1]))
        return out_list'''
        word_frequency = self.word_fq(keyword)  # Get frequency of each word
        print("After tokenize query:")
        for word, fq in word_frequency.items():
            print(word, fq)
        word_frequency = self.normalize_tfidf(word_frequency)  # get normalized value of each word
        print("After norm query;")
        for word, fq in word_frequency.items():
            print(word, fq)
        doc_score = self.calculate_cosine_similarity(word_frequency)  # return dict of doc with their score as value
        print("After cosine similarity: ")
        for doc, score in doc_score.items():
            print(doc, score)
        return sorted(doc_score.items(), key=lambda x: -x[1])[:K]
        # return dict(itertools.islice(doc_score.items(),K))


    def multi_query(self, multi_word, K):
        url_lst = []

        for word in multi_word.split():
            for doc_and_score in self.search_url(word, K):
                url_lst.append(doc_and_score)
        return sorted(url_lst, key=lambda x: -x[1])[:K]


    # Return a dict() with
    # token = DocID, value = score
    def calculate_cosine_similarity(self, word_frequency):
        doc_score = defaultdict(int)
        for qword, qnorm in word_frequency.items():
            for did, doc in self.normalized_tf.items():
                if qword in doc.keys():  # word in the document
                    doc_score[did] += qnorm * doc[qword]
        return doc_score


    # Calculate tfidf and normalize
    def normalize_tfidf(self, word_frequency):
        # Courpus Count
        total_documents = len(self.normalized_tf)
        query_length = 0
        for word, freq in word_frequency.items():
            # print(self.index.keys())
            # if word in index -> calculate tfidf
            if word in self.index.keys():
                print("In index")
                df = len(self.index[word])
                word_frequency[word] = 1 + math.log(freq, 10) * math.log(total_documents / df, 10)
                query_length += word_frequency[word] ** 2
            # else tfidf = 0
            else:
                print("Not in Index")
                word_frequency[word] = 0
        query_length = math.sqrt(query_length)
        for word, freq in word_frequency.items():
            if freq != 0:
                word_frequency[word] = freq / query_length
        return word_frequency


    # find word frequency in query
    def word_fq(self, word):
        query_token = word.split()
        query_dict = dict()
        for w in query_token:
            if w not in query_dict:
                query_dict[w] = 1
            else:
                query_dict[w] += 1
        return query_dict


    def search_length(self, keyword):
        if keyword in self.index.keys():
            return len(self.index[keyword])






