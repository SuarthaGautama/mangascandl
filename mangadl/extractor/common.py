
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


class MangaSiteExtractor:
    def  __init__(self,cwd):
        self.cwd = cwd

    def download_img(self,url,filename):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(self.cwd+'/'+str(filename)+".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    def get_soup(self,url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        rqst = opener.open(req)    
        if rqst.getcode() == 200:
            return BeautifulSoup(rqst, 'html5lib')
    
    def prepare_folder(self,folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    def download_batch(self,title_url,start,end,folder_name):
        self.cwd=self.cwd+'/'+folder_name
        page_number = 0
        self.prepare_folder(self.cwd)
        for i in range(int(start),int(end)+1):
            chapter_url = title_url+str(i)
            page_number = self.download_chapter(chapter_url,page_number,folder = self.cwd)
        print('download finished')

    def download_chapter(self,chapter_url,page_count = 0,folder = None):
        soup = self.get_soup(chapter_url)
        total_page = self.extract_total_page(soup)
        pbar = tqdm(total=total_page,desc=chapter_url)
        if not folder:
            folder_name = self.extract_title(soup)
            self.cwd = self.cwd + '/'+folder_name
            self.prepare_folder(self.cwd)
        for i in range(1,total_page+1):
            page_url = self.get_chapter_page(chapter_url,i)
            page_soup = self.get_soup(page_url)
            image_url = self.get_image_url(page_soup)
            self.download_img(image_url,page_count+i)
            pbar.update(1)
        pbar.close()
        return page_count+total_page

    def extract_title(self,soup):
        raise NotImplementedError("Please Implement this method")    

    def extract_total_page(self,soup):
        raise NotImplementedError("Please Implement this method")

    def get_chapter_page(self,chapter_url,page):
        raise NotImplementedError("Please Implement this method")

    def get_image_url(self,soup):
        raise NotImplementedError("Please Implement this method")