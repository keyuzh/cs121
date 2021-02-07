# crawler.py
# CS121 Winter 2021 Project 2: Web Crawler
# Group: 2
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

import logging
import re
from urllib.parse import urlparse

from lxml import etree, html

logger = logging.getLogger(__name__)


class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus, analytics):
        self.frontier = frontier
        self.corpus = corpus
        self.analytics = analytics

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched,
                        len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            current_count = 0  # count the number of valid out links
            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    current_count += 1
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)
            self.analytics.record_crawled_url(url)
            self.analytics.update_most_valid_links(url, current_count)

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.
        Suggested library: lxml
        """
        # use redirected url if possible
        if url_data['is_redirected'] and url_data['url'] != url_data['final_url']:
            url_data['url'] = url_data['final_url']
        # no content (404, etc.)
        if url_data['content'] is None:
            return []
        try:
            # html.fromstring can take both str and bytes object; but str can be dangerous and sometimes
            # raise unicode encoding exception, so we want to convert str to bytes
            if isinstance(url_data['content'], str):
                url_data['content'] = bytes(url_data['content'], encoding='utf8')
            string_document = html.fromstring(url_data['content'])
        except etree.ParserError:
            # html.fromstring() raises this exception when the content is invalid
            # e.g. http code is not 200; content encoding is not utf-8 and cannot decode;
            #      content does not exist in corpus and therefore url_data['content'] is None;
            return []
        # convert links to absolute link
        string_document.make_links_absolute(url_data['url'])
        # .iterlinks yields(element, attribute, link, pos) for every link in the document.
        # only want link to other websites (not images, etc.), add to final list only if 'href'
        # sometimes the link is between two lines and has a \n in between, remove that
        # outputLinks = [x[2].replace("\n", "") for x in string_document.iterlinks() if x[1] == 'href']
        outputLinks = [x[2] for x in string_document.iterlinks() if x[1] == 'href']
        # analytics: extract text from html and pass to analytics
        self.analytics.count_words(url_data['url'], string_document)
        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        # https://docs.python.org/3/library/urllib.parse.html
        # parsed.scheme = URL specifier
        # parsed.netloc = NetWork location Ex: www.uci.edu
        # parsed.path = path
        # parsed.params = parameter for last path element
        # parsed.query = query component
        # EX: scheme://netloc/path;parameters?query#fragment
        parsed = urlparse(url)

        # not even a webpage, no need to keep track of them
        if parsed.scheme not in set(["http", "https"]):
            return False

        path = (parsed.netloc, parsed.path)
        parameter = (parsed.params, parsed.query, parsed.fragment)

        first_time = False
        if path not in self.analytics.crawl_history.keys():
            # first time seeing this page, construct its inner dict
            self.analytics.crawl_history[path] = {
                "parameter": parameter,
                "is_trap": False
            }
            first_time = True

        # helper variable to shorten the lines or the code looks like Java
        inner_dict = self.analytics.crawl_history[path]

        # update parameters with the most recent one, while saving the old one
        old_parameter = inner_dict["parameter"]  # need to save this variable for later
        inner_dict["parameter"] = parameter

        if inner_dict["is_trap"]:
            # url is a known traps
            return False
        if len(url) > 300 or (0 < len(old_parameter[1]) < len(parsed.query)):
            # url is super long or the length of query gets longer every time -> trap
            inner_dict["is_trap"] = True
            self.analytics.record_trap(url)
            return False
        if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", url):
            # repeating sub-directory -> trap
            # regex from https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression
            inner_dict["is_trap"] = True
            self.analytics.record_trap(url)
            return False
        if not first_time and (old_parameter == parameter or len(parsed.fragment) > 0):
            # already seen this page, the parameter did not change or not in a meaningful way (e.g. simply take us to a
            # specific location of the page). the actual content of the page is the same, no point in crawling again
            return False
        # test against provided regex
        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" + "|c|cpp|cc|h|hpp|cs|java|py|json|asm|lif" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf|txt)$", parsed.path.lower())
        except TypeError:
            print("TypeError for ", parsed)
            return False