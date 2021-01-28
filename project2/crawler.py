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
        # self.crawlHistory = {} #Dictionary to story crawl history
        # self.traps = [] #list that story all the known traps url
        # self.most_valid_links = 0 #
        # self.most_valid_page = None #

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
        outputLinks = []
        # print(f"parsing: {url_data['url']}")
        # print(f"response code: {url_data['http_code']}")
        # print(f"type: {url_data['content_type']}")
        # if (
        #         # page must be valid (http 200)
        #         url_data['http_code'] != 200
        #         # content must be html and in utf-8 encoding (I dont know why url_data['content_type'] is a str
        #         # representing a bytes object, but anyways, it is what it is)
        #         or url_data['content_type'] != "b'text/html; charset=UTF-8'"
        #         # content must exist in corpus
        #         or url_data['content'] is None
        # ):
        #     return []

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
        except Exception as e:
            print(e)
            raise
        # convert links to absolute link
        string_document.make_links_absolute(url_data['url'])
        # .iterlinks yields(element, attribute, link, pos) for every link in the document.
        # only want link to other websites (not images, etc.), add to final list only if 'href'
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

        first_half = parsed.netloc + parsed.path  # create new string with the domain + path
        second_half = parsed.params + parsed.query + parsed.fragment

        if first_half not in self.analytics.crawlHistory.keys():
            # first time seeing this page, construct its inner dict
            self.analytics.crawlHistory[first_half] = {
                "second_half": second_half,
                "seen_times": 0,
                "is_trap": False
            }

        # helper variable to shorten the lines or the code looks like Java
        inner_dict = self.analytics.crawlHistory[first_half]
        # increment the number of times seen
        inner_dict["seen_times"] += 1

        # always use the newest second_half
        old_second_half_length = len(inner_dict["second_half"])
        inner_dict["second_half"] = second_half

        if inner_dict["is_trap"]:
            # url is a known traps
            return False
        if len(url) > 300 or len(second_half) > old_second_half_length:
            # url is super long or it gets longer each time
            inner_dict["is_trap"] = True
            return False
        if inner_dict["seen_times"] > 10:
            # browse same page over 10 times --> trap, loop
            # inner_dict["is_trap"] = True
            return False
        # test against provided regex
        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf|txt)$", parsed.path.lower())
        except TypeError:
            print("TypeError for ", parsed)
            return False
