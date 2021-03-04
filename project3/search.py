# search.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

import math
from collections import defaultdict
from pathlib import Path

from corpus import Corpus


class Search:
    def __init__(self, corpus_path: str or Path, index: dict, normalized_tf: dict, tag: dict, bi_index=None, bi_tf=None):
        self.corpus = Corpus(corpus_path)
        self.index = index
        self.normalized_tf = normalized_tf
        self.html_tag = tag
        self.bigram_index = bi_index
        self.bigram_tf = bi_tf

    # search return at most K urls where K = 20 in this case
    def search(self, keyword, num=20) -> (int, (str, float)):
        keyword_list = keyword.split()
        if len(keyword_list) == 1:
            return self.search_single_word(keyword, num)
        bigrams = [" ".join([keyword_list[i], keyword_list[i+1]]) for i in range(len(keyword_list)-1)]
        return self.search_multi_word(keyword, bigrams, num)

    def search_single_word(self, keyword, num=20):
        # no need to normalize for single word
        query_word_frequency = {keyword: 1}
        # return dict of doc with their score as value
        doc_score = self.calculate_cosine_similarity(query_word_frequency, self.normalized_tf)
        return len(doc_score), sorted(doc_score.items(), key=lambda x: -x[1])[:num]

    def search_multi_word(self, keyword, bigram_list, num=20):
        query_word_frequency = self.word_fq(keyword)  # Get frequency of each word
        self.normalize(query_word_frequency)  # get normalized value of each word
        # first calculate the scores using single word
        doc_score = self.calculate_cosine_similarity(query_word_frequency, self.normalized_tf)
        # then add bi-gram results
        if self.bigram_tf is not None:
            for bigram in bigram_list:
                bigram_score = self.calculate_cosine_similarity({bigram: 1}, self.bigram_tf)
                for path, score in bigram_score.items():
                    doc_score[path] += score * 2
        return len(doc_score), sorted(doc_score.items(), key=lambda x: -x[1])[:num]

    def calculate_cosine_similarity(self, word_frequency, normalized_tf) -> {str: float}:
        """use cosine similarity method to calculate the relevance score for each page"""
        # Return a dict() with key = DocID, value = score
        doc_score = defaultdict(int)
        for query_word, query_normalized_score in word_frequency.items():
            for path, document_frequencies in normalized_tf.items():
                if query_word in document_frequencies.keys():
                    # find html tag score and use it as a multiplier
                    tag_score = self.get_html_tag_score(query_word, path)
                    doc_score[path] += query_normalized_score * document_frequencies[query_word] * tag_score
        return doc_score

    def get_html_tag_score(self, query: str, doc_id: str) -> float:
        """find the tag with the highest importance, and return a multiplier for that tag"""
        scores = {
            'title': 1.5,
            'h1': 1.4,
            'h2': 1.4,
            'h3': 1.3,
            'h4': 1.3,
            'h5': 1.2,
            'h6': 1.2,
            'b': 1.1,
            'strong': 1.1
        }
        try:
            return max([scores[tag] for tag in self.html_tag[doc_id][query]])
        except (KeyError, ValueError):
            # no tag, use default value
            return 1

    def normalize(self, word_frequency: dict) -> dict:
        """normalize the query (vector) for cosine similarity calculation"""
        # Corpus Count
        total_documents = len(self.normalized_tf)
        query_length = 0
        # sum the squared results then sqrt
        for word, freq in word_frequency.items():
            # if word in index -> normalize
            if word in self.index.keys():
                df = len(self.index[word])
                word_frequency[word] = 1 + math.log(freq, 10) * math.log(total_documents / df, 10)
                query_length += word_frequency[word] ** 2
            else:
                word_frequency[word] = 0
        query_length = math.sqrt(query_length)
        # divide by length
        for word, freq in word_frequency.items():
            if freq != 0:
                word_frequency[word] = freq / query_length
        # return word_frequency

    def word_fq(self, word):
        """find word frequency in query"""
        query_token = word.split()
        query_dict = dict()
        for w in query_token:
            if w not in query_dict:
                query_dict[w] = 1
            else:
                query_dict[w] += 1
        return query_dict
