
import shutil
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from http.cookiejar import CookieJar
import requests
import urllib
from urllib.request import urlparse
from tqdm import tqdm
import argparse
import os
import threading
from .model import MangaPage


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MangaUrlError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """
    default_msg = 'Manga not found in url, Please check the url'
    def __init__(self, expr, msg = default_msg):
        self.expr = expr
        self.msg = msg

class Utility(object):
    @staticmethod
    def get_soup(url):
        page = requests.get(url)
        if page.status_code == 200:
            return BeautifulSoup(page.text,'html.parser')


class BulkImageDownloader(threading.Thread):
    def __init__(self, queue, destfolder,progressBar,image_url_parser):
        super(BulkImageDownloader, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True
        self.prepare_folder(destfolder)
        self.progressBar = progressBar
        self.image_url_parser = image_url_parser
        
    def run(self):
        while True:
            manga_page = self.queue.get()
            try:
                image_url = self.image_url_parser(manga_page.url)
                self.download_img(image_url,manga_page.pageIndex)
            except Exception as e:
                print("   Error: %s"%e)
            self.queue.task_done()

    def download_img(self,url,page_number):
        filename = str(page_number)+".jpg"
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(self.destfolder+'/'+filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                self.progressBar.update(1)
    
    def prepare_folder(self,folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    def get_soup(self,url):
        page = requests.get(url)
        if page.status_code == 200:
            return BeautifulSoup(page.text,'html.parser')


class MangaSiteExtractor:
    def  __init__(self,cwd,number_of_thread=4):
        self.cwd = cwd
        self.number_of_thread = number_of_thread

    def download_img(self,url,filename):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(self.cwd+'/'+str(filename)+".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    def get_soup(self,url):
        page = requests.get(url)
        if page.status_code == 200:
            return BeautifulSoup(page.text,'html.parser')
        
        
    def prepare_folder(self,folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    def download_batch(self,title_url,start,end,folder_name=None):
        if folder_name:
            self.cwd=self.cwd+'/'+folder_name
        if not title_url.endswith('/'):
            title_url = title_url+'/'
        page_number = 0
        self.prepare_folder(self.cwd)
        chapter_url_list = self.get_chapter_url_to_download(title_url,start,end)
        try:
            for chapter_url in chapter_url_list:
                
                if folder_name:
                    page_number = self.download_chapter(chapter_url,page_number,folder = self.cwd)
                else:
                    soup = self.get_soup(chapter_url)
                    page_number = self.download_chapter(chapter_url)
            print('download finished')
        except MangaUrlError as e:
            print(e.msg)
