# PartA.py
# CS121 Winter 2021 Project 1
# Name: Keyu Zhang
# ID: 19898090
# UCINetID: keyuz4

############################################################################
##  PART A: Word Frequencies:                                             ##
##   Description:                                                         ##
##      Run on command line using command:                                ##
##          python PartA.py [filename]                                    ##
##   Input: [filename] - the path to a txt file                           ##
##   Output: prints tokens and frequencies                                ##
##                                                                        ##
##   Source: https://canvas.eee.uci.edu/courses/32171/assignments/623046  ##
##   (Header Uploaded by Will Schallock, last updated 1/5/21)             ##
############################################################################
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
        for k, v in sorted(frequencies.items(), key=lambda x: (-x[1], x[0])):
            print(k, '\t', v, sep='')


if __name__ == '__main__':
    input_dict = {
        'in': 2, 'live': 2,
        'fact': 1, 'fun': 1, 'here': 1, 'india': 1, 'mostly': 2, 'a': 1, 'africa': 1,
    }
    a = WordFrequencies()
    a.print(input_dict)
    print(sys.argv)
    file_path = Path(sys.argv[1])
    print(file_path, type(file_path))
    pass

