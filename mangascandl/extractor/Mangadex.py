from .common import MangaSiteExtractor
from .common import MangaUrlError
from .common import BulkImageDownloader
import json
import requests
from urllib.parse import urlparse,urljoin
import queue
from .model import MangaPage
from tqdm import tqdm
from collections import OrderedDict
class Mangadex(MangaSiteExtractor):
    '''crawler for https://mangadex.org'''
    mangadex_url = 'https://mangadex.org/'
    mangadex_api_url_base = mangadex_url + 'api/'
    chapter_url = mangadex_api_url_base+'chapter/'
    manga_url = mangadex_api_url_base+'manga/'
    manga_info = None

    def url_join(self,host,*additional_path):
        for i in additional_path:
            host = urljoin(host,i)
        return host

    def download_chapter(self,chapter_url,page_count = 0,folder = None):
        url_object = urlparse(chapter_url)
        paths = url_object.path.split('/')
        download_queue = queue.Queue()
        save_path = self.cwd
        if paths[1] == 'chapter':
            chapter_code = paths[2]
        else:
            raise MangaUrlError('[ERROR] Manga page list is not found')
        
        chapter_info = self.get_chapter_info(chapter_code)
        image_arr = chapter_info['page_array']
        total_page = len(image_arr)
        manga_info = self.get_manga_info(chapter_info['manga_id'])
        pbar = tqdm(total=total_page,desc=chapter_url)
        if not folder:
            folder_name = manga_info['manga']['title']+' '+chapter_info['chapter']
            save_path = self.cwd + '/'+folder_name
            self.prepare_folder(save_path)
        for page_index in range(1,total_page+1):
            page_url = self.url_join(self.mangadex_url,chapter_info['server'],chapter_info['hash']+'/',image_arr[page_index-1])
            download_queue.put(MangaPage(page_url,page_count+page_index))
        for i in range(self.number_of_thread):
            t = BulkImageDownloader(download_queue,save_path,pbar,self.get_image_url)
            t.start()
        download_queue.join()
        pbar.close()
        return page_count+total_page

    def get_image_url(self,url):
        return url

    def get_chapter_info(self,chapter_code):
        return self.request_api(self.chapter_url + chapter_code)
        
    
    def get_manga_info(self,manga_code):
        if self.manga_info is None:
            headers = {'Content-Type': 'application/json'}
            response = requests.get(self.manga_url+str(manga_code))
            if response.status_code == 200:
                self.manga_info = json.loads(response.content.decode('utf-8'))
                return self.manga_info
            else:
                return None
        else:
            return self.manga_info
    
    def request_api(self,url,headers={'Content-Type': 'application/json'} ):
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    def get_chapter_url_to_download(self,url,start,end):
        manga_code = self.get_manga_code_from_manga_url(url) 
        manga_info = self.get_manga_info(manga_code)
        all_chapter_list = manga_info['chapter']
        ordered_chapter = {}
        for chapter_code,chapter_info in all_chapter_list.items() :
            chapter_index = float(chapter_info['chapter'])
            if chapter_index >= float(start) and chapter_index <= float(end) and chapter_info['lang_code'] == 'gb':
                ordered_chapter[chapter_index] = 'http://mangadex.org/chapter/'+chapter_code
        
        ordered_chapter = OrderedDict(sorted(ordered_chapter.items()))
        return list(ordered_chapter.values())
     
    def get_manga_code_from_manga_url(self,url):
        url_object = urlparse(url)
        paths = url_object.path.split('/')
        if len(paths) >= 3:
            return paths[2]

