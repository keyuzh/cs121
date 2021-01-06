# PartA.py
# CS121 Winter 2021 Project 1
# Name: Keyu Zhang
# ID: 19898090
# UCINetID: keyuz4
from pathlib import Path
import sys
from collections import defaultdict


class WordFrequencies:
    def tokenize(self, TextFilePath: str or Path) -> ['token']:
        """reads in a text file and returns a list of the tokens in that file.
        a token is a sequence of alphanumeric characters independent of capitalization"""
        pass

    def computeWordFrequencies(self, tokens: ['token']) -> {'token': int}:
        """counts the number of occurrences of each token in the token list,
        returns a dict where the keys are the tokens and the values are the number of occurrences"""
        frequencies = defaultdict(int)
        for token in tokens:
            frequencies[token] += 1
        return frequencies

    def print(self, frequencies: {'token': int}):
        """prints out the word frequency counts onto the screen, ordered by decreasing frequency,
        ties are sorted alphabetically and in ascending order."""
        for k, v in sorted(
                frequencies.items(),
                key=lambda x: (-x[1], x[0])
        ):
            print(f"{k}\t{v}")


if __name__ == '__main__':
    input_dict = {
        'in': 2, 'live': 2, 'mostly': 2, 'a': 1, 'africa': 1,
        'fact': 1, 'fun': 1, 'here': 1, 'india': 1
    }
    a = WordFrequencies()
    a.print(input_dict)