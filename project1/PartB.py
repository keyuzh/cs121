# PartB.py
# CS121 Winter 2021 Project 1
# Name: Keyu Zhang
# ID: 19898090
# UCINetID: keyuz4
############################################################################
##  Part B: Intersection of two files:                                    ##
##   Description:                                                         ##
##      Run on command line using command:                                ##
##          python PartB.py [filename1] [filename2]                       ##
##   Input: [filename1] - the path to a txt file                          ##
##          [filename2] - the path to a txt file                          ##
##   Output: prints the number of tokens file1 and file2 have in common   ##
##                                                                        ##
##   Source: https://canvas.eee.uci.edu/courses/32171/assignments/623046  ##
##   (Header Uploaded by Will Schallock, last updated 1/5/21)             ##
############################################################################

import sys

from PartA import WordFrequencies


def token_intersection(token1: ['tokens'], token2: ['tokens']) -> int:
    """
    given two list of tokens, find the number of common words (intersection) between them
    :parameter: two lists of tokens
    :returns: number of tokens the two lists have in common
    :complexity: O(n) time
        construction of two sets: O(len(token1)) + O(len(token2)) -> O(n) + O(n)
        intersection of two sets: O(len(set1) + len(set2)) -> O(n) + O(n)
        finding the length of set: O(1)
        simplify:
            O(len(token1)) + O(len(token2)) + O(len(set1) + len(set2)) + O(1)
            -> O(4n + 1)
            -> O(n)
    """
    return len(set(token1) & set(token2))


def main():
    """
    given path to 2 text files from terminal; tokenize both files, and find the number of intersecting words
    between the 2 token lists, print the number on the terminal
    :return: None
    """
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    wf = WordFrequencies()
    token1 = wf.tokenize(file1)
    token2 = wf.tokenize(file2)
    print(token_intersection(token1, token2))


if __name__ == "__main__":
    main()
