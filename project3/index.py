# index.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

# construct inverted index with key=token, value=where the token occur; TF-IDF, etc

from collections import defaultdict
import pickle
import math
from pathlib import Path


class Index:
    def __init__(self, bookkeeping_json, bigram=False):
        self.index_filename = "inverted_index"
        self.tf_filename = "normalized_tf"
        self.bigram = bigram
        if bigram:
            self.index_filename += "_bigram"
            self.tf_filename += "_bigram"
        self.book = bookkeeping_json
        # inverted_index will be a dict of sets,
        # the keys will be the tokens, values will be a set of tuples, storing the url, file path, and tf-idf score
        # {
        #     'token': list( [docID, frequency, tf-idf, pos] )
        #     'irvine': list( [0/0, 15, .123, {'title'}], [3/5, 13, .123, {'h1'}] )
        # }
        self.inverted_index = defaultdict(list)

        # inverted_index will be a dict of sets,
        # the keys will be the tokens, values will be a set of tuples, storing the url, file path, and tf-idf score
        # {
        #     'token': {docID: pos}
        #     'irvine': dict (0/0: {'title'}, {3/5: {'h1'})
        # }
        self.tags = defaultdict(dict)

        # container to temporarily store the word frequencies in each web page
        # {
        #   path : {'open': 11, 'source': 11, 'project': 11, 'slide': 1, '50': 1}
        # }
        self.frequencies = dict()

        # stores what position that the given word appears
        # {
        #   path : {'open': {'title', h1}, 'source': {'title', 'h2'} }
        # }
        self.positions = dict()

        # stores the normalized tfidf score in each document
        # {
        #     path : {'word': normalized_tfidf}
        # }
        self.tfidf = dict()

    def insert(self, path, frequencies: dict, positions=dict()):
        """insert the result of a document into temporary container"""
        self.frequencies[path] = frequencies
        if not self.bigram:
            self.positions[path] = positions

    def normalize_tf(self):
        """normalize tf score in each document"""
        for doc in self.frequencies.values():
            for word, freq in doc.items():
                doc[word] = 1 + math.log(doc[word], 10)
            tf_factor = math.sqrt(sum([tf**2 for tf in doc.values()]))
            for word, freq in doc.items():
                doc[word] = doc[word] / tf_factor

    def calculate_tfidf(self):
        """calculate tfidf for every word in the document"""
        total_documents = len(self.frequencies)  # N
        for token, occurrences in self.inverted_index.items():
            df = len(occurrences)
            for occ in occurrences:
                tf = occ[1]
                tfidf = (1 + math.log(tf, 10)) * math.log(total_documents / df, 10)
                occ[2] = tfidf

    def write_file(self):
        """save the inverted index and normalized tf into a local file"""
        data_dir = Path("./data")
        index_path = data_dir / self.index_filename
        tf_path = data_dir / self.tf_filename
        pickle.dump(self.inverted_index, open(index_path, "wb"))
        pickle.dump(self.frequencies, open(tf_path, "wb"))
        if not self.bigram:
            # save html tag info
            tag_path = data_dir / "html_tag"
            pickle.dump(self.positions, open(tag_path, 'wb'))

    def build(self):
        """calculate normalized tfidf and save the file"""
        self.normalize_tf()
        for path, word_freqs in self.frequencies.items():
            for token, fq in word_freqs.items():
                # add to inverted index
                self.inverted_index[token].append([path, fq, 0])
        # calculate tfidf, then save
        self.calculate_tfidf()
        self.write_file()
