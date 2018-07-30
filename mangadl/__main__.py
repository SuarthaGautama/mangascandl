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


cwd = os.getcwd()

def download_img(url,filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(cwd+'/'+str(filename)+".jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        
def get_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    rqst = opener.open(req)    
    if rqst.getcode() == 200:
        return BeautifulSoup(rqst, 'html5lib')

def download_chapter(chapter_url,page_count = 0,folder = None):
    soup = get_soup(chapter_url)
    page_select = soup.find('select',{'id':'pageMenu'})
    childs = page_select.findChildren()
    total_page = len(childs)
    pbar = tqdm(total=total_page,desc=chapter_url)
    if not folder:
        page_title = soup.find('title').text
        folder_name = page_title.split('-')[0]
        global cwd
        cwd = cwd + '/'+folder_name
        prepare_folder(cwd)
    for i in range(1,total_page+1):
        page_url = chapter_url+"/"+str(i)
        page_soup = get_soup(page_url)
        image_div = page_soup.find('div',{"id": "imgholder"})
        image_url = image_div.find('img')['src']
        download_img(image_url,page_count+i)
        pbar.update(1)
    pbar.close()
    return page_count+total_page

def prepare_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def download_batch(title_url,start,end,folder_name):
    global cwd
    cwd=cwd+'/'+folder_name
    page_number = 0
    prepare_folder(cwd)
    for i in range(int(start),int(end)+1):
        chapter_url = title_url+str(i)
        page_number = download_chapter(chapter_url,page_number,folder = cwd)
    print('download finished')

def main():

    arger = argparse.ArgumentParser(usage="%(prog)s [download|batch]")
    subparsers = arger.add_subparsers(dest="command")
    download_single_parser = subparsers.add_parser("download")
    download_single_parser.add_argument("chapter_url")
    download_single_parser.add_argument("destination_folder",nargs='?')

    download_batch_parser = subparsers.add_parser('batch')
    download_batch_parser.add_argument("title_url")
    download_batch_parser.add_argument("starting_chapter")
    download_batch_parser.add_argument("end_chapter")
    download_batch_parser.add_argument("destination_folder")

    opts = arger.parse_args()

    if opts.command == 'download':
        if opts.destination_folder:
            cwd = opts.destination_folder
        download_chapter(opts.chapter_url,0)
    elif opts.command == 'batch':
        download_batch(opts.title_url,opts.starting_chapter,opts.end_chapter,opts.destination_folder)

if __name__ == '__main__':
    main()