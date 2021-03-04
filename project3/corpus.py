import json
from pathlib import Path

import lxml.html


def json_to_dict(json_path: Path or str) -> dict:
    """load json to a dict"""
    with open(json_path, encoding='utf8') as json_file:
        return json.load(json_file)


class Corpus:
    def __init__(self, corpus_path: str or Path):
        self.path = Path(corpus_path)
        # dict to convert path to url
        self.bookkeeping = json_to_dict(self.path / "bookkeeping.json")

    def feed_html(self) -> dict:
        """generator that yields html from local corpus"""
        for path, url in self.bookkeeping.items():
            html_content = self.get_html(path)
            yield (html_content, url, path)

    def get_html(self, path: str) -> str:
        """retrieve the webpage html from corpus and return the content as string"""
        with self.get_file(path) as f:
            return f.read()

    def get_file(self, path) -> open:
        """retrieve the webpage as an open file"""
        # path_list = path.split('/')
        # directory = path_list[0]
        # file = path_list[1]
        file_path = self.path / path
        return open(file_path, encoding='utf8')

    def get_bookkeeping(self):
        """returns the bookkeeping dict"""
        return self.bookkeeping

    def get_url(self, path: str) -> str:
        """get the url of the webpage given the path"""
        return self.bookkeeping[path]

    def get_title(self, path: str) -> str:
        """returns the title of the given web page"""
        title = lxml.html.parse(self.get_file(path)).find(".//title")
        if title is None:
            return "(Description not found)"
        return title.text.replace('\n', '')
