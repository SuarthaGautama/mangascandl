import shutil
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from http.cookiejar import CookieJar
import requests
import urllib
from urllib.request import urlparse
from urllib.parse import urlparse
from tqdm import tqdm
import argparse
import os
from .extractor.Mangareader import Mangareader
from .extractor.Mangadex import Mangadex
cwd = os.getcwd()

def main():
    global cwd
    extractor = Mangareader(cwd)
    arger = argparse.ArgumentParser(usage="%(prog)s [download|batch]")
    subparsers = arger.add_subparsers(dest="command")
    download_single_parser = subparsers.add_parser("download")
    download_single_parser.add_argument("chapter_url")
    download_single_parser.add_argument("destination_folder",nargs='?')

    download_batch_parser = subparsers.add_parser('batch')
    download_batch_parser.add_argument("title_url")
    download_batch_parser.add_argument("starting_chapter")
    download_batch_parser.add_argument("end_chapter")
    download_batch_parser.add_argument("destination_folder",nargs='?')

    
    opts = arger.parse_args()

    if opts.command == 'download':
        if opts.destination_folder:
            cwd = opts.destination_folder
        extractor = getExtractor(opts.chapter_url)
        extractor.download_chapter(opts.chapter_url,0)
    elif opts.command == 'batch':
        extractor = getExtractor(opts.title_url)
        extractor.download_batch(opts.title_url,opts.starting_chapter,opts.end_chapter,opts.destination_folder)
        
def getExtractor(url):
    url_pattern = ['']
    o = urlparse(url)
    if o.netloc == 'mangadex.org':
        extractor = Mangadex(cwd)
    elif o.netloc.endswith('mangareader.net'):
        extractor = Mangareader(cwd)
    return extractor
    
if __name__ == '__main__':
    main()