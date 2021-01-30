# analytics.py
# CS121 Winter 2021 Project 2: Web Crawler
# Group: 2
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

from collections import defaultdict
from urllib.parse import urlparse

from lxml.html.clean import Cleaner

from project1 import WordFrequencies


class Analytics:
    def __init__(self):
        # frequencies is a dict that stores the frequencies of word, or tokens, after the crawler has crawled the page
        # and extracted the text from html
        self.wf = WordFrequencies()
        self.frequencies = dict()

        # crawlHistory is a nested dict that stores the following info:
        #     - full url, separated into two parts after parsing with urllib.parse.urlparse
        #           > the first part is the path of webpage, this is used as the key of the outer dict,
        #             to identify whether the exact webpage has been crawled or not
        #           > the second part is the dynamic part of this webpage; includes query, parameter, fragment
        #             this is stored as a value in the inner dict, it is updated each time that the web page is seen by
        #             is_valid() function in crawler.py
        #     - whether this page is considered a crawler trap

        # The structure of this dict is as follows:
        #       example url: https://www.ics.uci.edu/community/news/view_news?id=1473
        # {
        #     "path": (str, str)                tuple(netloc, path) ex. (www.ics.uci.edu, /community/news/view_news)
        #     {
        #         "parameter": (str, str, str)  tuple(urlparse.params, urlparse.query, urlparse.fragment)
        #                                       ex. ("", "id=1473", "")
        #         "is_trap": bool               whether the page has been marked as a trap
        #     }
        # }
        self.crawl_history = dict()  # Dictionary to story crawl history

        # collection of all crawled (valid) urls, used for analytics #1 and #3
        self.downloaded_urls = list()

        # collection of all traps
        self.traps = list()

        # tuple containing the url with the most valid out links
        self.most_valid_page = (None, 0)

        # tuple containing the url of the page with the most words and the number of words
        self.longest_page = (None, 0)

        # set of english stopwords, stored in a separate text file
        self.stopwords = self._get_stopwords("stopwords.txt")

    def _get_stopwords(self, file: str):
        with open(file, 'r') as f:
            return eval(f.read())

    def _write_line(self, file: open, line: str):
        # write the given str as a single line
        # use this method to write to file so you can forget \n
        file.write(line.replace('\n', '') + '\n')

    def write_crawl_history(self):
        """
        Analytics #1: Keep track of the subdomains that it visited, and count how many different URLs it has
        processed from each of those subdomains.
        """
        # dict to keep track of the number crawled in each subdomain
        subdomain = defaultdict(int)
        for url in self.downloaded_urls:
            subdomain[urlparse(url).netloc] += 1
        with open("analytics_1_subdomains.txt", "w", encoding='utf8') as f:
            self._write_line(f, "Subdomains\tCount")
            # for better formatting, sort the output by largest crawl count
            for url, count in sorted(subdomain.items(), key=lambda x: (-x[1], x[0])):
                self._write_line(f, f"{url}\t{count}")

    def write_most_valid_page(self):
        """
        Analytics #2: Find the page with the most valid out links (of all pages given to your crawler). Out Links are
        the number of links that are present on a particular webpage.
        """
        with open("analytics_2_most_valid_page.txt", "w", encoding='utf8') as f:
            self._write_line(f, "Page with the most valid out links:")
            self._write_line(f, str(self.most_valid_page[0]))
            self._write_line(f, "Number of out links:")
            self._write_line(f, str(self.most_valid_page[1]))

    def write_url_traps(self):
        """
        Analytics #3: List of downloaded URLs and identified traps.
        """
        with open("analytics_3_url_and_traps.txt", "w", encoding='utf8') as f:
            self._write_line(f, "List of valid urls and traps")
            self._write_line(f, "url:")
            for url in self.downloaded_urls:
                self._write_line(f, f"    {url}")
            self._write_line(f, "=" * 25)
            self._write_line(f, "")
            self._write_line(f, "traps:")
            for url in self.traps:
                self._write_line(f, f"    {url}")

    def write_longest_page(self):
        """
        Analytics #4: the longest page in terms of number of words
        """
        with open("analytics_4_longest_page.txt", 'w', encoding='utf8') as f:
            self._write_line(f, "Longest page in terms of number of words:")
            self._write_line(f, str(self.longest_page[0]))
            self._write_line(f, "Number of words:")
            self._write_line(f, str(self.longest_page[1]))

    def write_common_words(self):
        """
        Analytics #5 the 50 most common words in the entire set of pages
        """
        with open("analytics_5_most_common_words.txt", 'w', encoding='utf8') as f:
            self._write_line(f, "50 most common words:")
            self._write_line(f, "Word\tCount")
            for word in self.wf.print(self.frequencies)[:50]:
                self._write_line(f, word)

    def write_all(self):
        self.write_crawl_history()
        self.write_most_valid_page()
        self.write_url_traps()
        self.write_longest_page()
        self.write_common_words()

    def update_most_valid_links(self, url: str, count: int):
        if count > self.most_valid_page[1]:
            self.most_valid_page = (url, count)

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
        # code from: https://stackoverflow.com/questions/8554035/
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter
        cleaned = cleaner.clean_html(html)
        return cleaned.text_content()

    def record_crawled_url(self, url: str):
        # add a valid url into the set of downloaded urls
        self.downloaded_urls.append(url)

    def record_trap(self, url: str):
        # add a trap to the set of traps
        self.traps.append(url)
