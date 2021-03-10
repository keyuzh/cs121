CS121 Winter 2021 Project 3: Search Engine
Group: 6
Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
UCINetID: keyuz4, cwlo1, emanuel1


external libraries used:
    lxml
        $ python3 -m pip install lxml

        lxml library is used to parse html webpages in the corpus

    nltk
        $ python3 -m pip install nltk

        NLTK requires Python versions 3.5, 3.6, 3.7, or 3.8
        - before building the inverted index, install required packages by
          running the following commands in *python console*
        >>> import nltk
        >>> nltk.download()
        - in the menu, choose to download all packages

    PyQt5
        $ python3 -m pip install PyQt5

        Qt library is used to implement GUI functionalities


project directory structure:
    data/               # initially empty, used to store data of inverted index
    project2/           # code from previous projects, included for dependencies
    build.py            # run this module to build the inverted index
    cli.py              # functions for CLI interface
    corpus.py           # retrieve information from corpus
    gui.py              # functions for GUI interface
    guiLogo.png         # Logo displayed in GUI
    index.py            # includes functions for index building
    interface.py        # run this module to start use the search engine
    lemmatization.py    # module to parse and lemmatize web pages
    readme.txt          # this file
    search.py           # module to retrieve search results from index
    stopwords.txt       # set of stop words


Running the Search Engine:
    Before running any modules, make sure you have installed all dependencies

    Run <build.py> to build the inverted index
    optional arguments:
        [-c <path> | --corpus=<path>]   specifies the directory of corpus, default="./WEBPAGES_RAW"
        [-b | --bigram]                 if specified, build the bigram index instead of normal index
    example:
        $ python3 build.py              use default corpus location and build normal index
        $ python3 build.py -b           use default corpus location and build bigram index
        $ python3 build.py -c ~/Desktop/WEBPAGES_RAW --bigram
                                        build bigram index using "~/Desktop/WEBPAGES_RAW" as corpus path

    Run <interface.py> to run the search engine (after index is built)
    optional arguments:
        [-c <path> | --corpus=<path>]   specifies the directory of corpus, default="./WEBPAGES_RAW"
        [-i <path> | --index=<path>]    specifies the directory of index, default="./data"
        [-b | --bigram]                 if specified, the bigram index is loaded IN ADDITION to normal index
                                        loading bigram is disabled by default since it increase load time by about 3x
        [-g | --gui]                    use the graphical interface instead of command line interface

    example:
        $ python3 interface.py          use default corpus and index location, launch CLI
        $ python3 interface.py -g       use default corpus and index location, launch GUI
        $ python3 interface.py -g -b -i ~/data
                                        use default corpus location, load index from "~/data", load bigram index and GUI
