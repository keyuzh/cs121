# 1. Keep track of the subdomains that it visited, and count how many different URLs it has
# processed from each of those subdomains.
# 2. Find the page with the most valid out links (of all pages given to your crawler). Out Links are the
# number of links that are present on a particular webpage.
# 3. List of downloaded URLs and identified traps.
# 4. What is the longest page in terms of number of words? (HTML markup doesn’t count as words)
# 5. What are the 50 most common words in the entire set of pages? (Ignore English stop words,
# which can be found, (https://www.ranks.nl/stopwords)

from project1 import WordFrequencies

import lxml
from lxml.html.clean import Cleaner


class Analytics:
    def __init__(self):
        self.wf = WordFrequencies()
        self.frequencies = dict()
        self.crawlHistory = {} #Dictionary to story crawl history
        self.traps = [] #list that story all the known traps url
        self.most_valid_links = 0
        self.most_valid_page = None
        # tuple containing the url of the page with the most words and the number of words
        self.longest_page = (None, 0)
        self.stopwords = self._get_stopwords("stopwords.txt")

    def _get_stopwords(self, file: str):
        with open(file, 'r') as f:
            return eval(f.read())

    def _write(self, file: open, line: str):
        # use this method to write to file so you can forget \n
        file.write(line + '\n')

    def write_crawl_history(self):
    #
        with open("crawl_history.txt", "w") as f:
            for key, value in self.crawlHistory.items():
                f.write(f"{key:<30}{value:>10}\n")

    def write_most_valid_page(self):
        # update format
        with open("most_valid_page.txt", "w") as f:
            self._write(f, "Page with the most valid out links:")
            self._write(f, str(self.most_valid_page))
            self._write(f, "Number of out links:")
            self._write(f, str(self.most_valid_links))

    def write_url_traps(self):
        #
        with open("url_and_traps.txt", "w") as f:
            f.write("url:\n")
            for key in self.crawlHistory.keys():
                f.write("  " + key + "\n")

            f.write("\nTraps:\n")
            for item in self.traps:
                f.write("  " + item + "\n")

    def write_longest_page(self):
        with open("longest_page.txt", 'w') as f:
            self._write(f, "Longest page in terms of number of words:")
            self._write(f, str(self.longest_page[0]))
            self._write(f, "Number of words:")
            self._write(f, str(self.longest_page[1]))

    def write_common_words(self):
        with open("most_common_words.txt", 'w') as f:
            self._write(f, "50 most common words:")
            self._write(f, '\n'.join(self.wf.print(self.frequencies)[:50]))

    def write_all(self):
        self.write_crawl_history()
        self.write_most_valid_page()
        self.write_url_traps()
        self.write_longest_page()
        self.write_common_words()

    def update_most_valid_links(self, url: str, count: int):
        if count > self.most_valid_links:
            self.most_valid_links = count
            self.most_valid_page = url

    def count_words(self, url: str, html: str):
        # extract text from html
        text = self._extract_text(html)
        # use tokenize() method from project1
        tokens = self.wf.tokenize(text)
        # analytics #4: find the longest page in terms of number of words
        num_of_words = len(tokens)
        if num_of_words > self.longest_page[1]:
            self.longest_page = (url, num_of_words)
        # analytics #5: most common words
        self.wf.computeWordFrequencies(tokens, self.frequencies, self.stopwords)

    def _extract_text(self, html: str) -> str:
        # remove html markup and javascript
        # https://stackoverflow.com/questions/8554035/remove-all-javascript-tags-and-style-tags-from-html-with-python-and-the-lxml-mod
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter

        # print("WITH JAVASCRIPT & STYLES")
        # print(lxml.html.tostring(lxml.html.parse('http://www.google.com')))
        # print("WITHOUT JAVASCRIPT & STYLES")
        cleaned = cleaner.clean_html(html)
        return cleaned.text_content()
