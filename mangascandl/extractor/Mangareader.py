from .common import MangaSiteExtractor
from .common import MangaUrlError
from .common import BulkImageDownloader
from tqdm import tqdm
import queue
from .model import MangaPage
from .common import Utility
class Mangareader(MangaSiteExtractor):
    '''crawler for https://www.mangareader.net'''


    def extract_title(self,soup):
        chapter_title_element = soup.find('title')
        if chapter_title_element is None:
            raise MangaUrlError('manga title is not found')
        else:
            chapter_title = chapter_title_element.text
            chapter_title = chapter_title.split('- Read')[0]
            return chapter_title

    def extract_total_page(self,soup):
        page_list = soup.find('select',{'id':'pageMenu'})
        if page_list is None:
            raise MangaUrlError('manga page list is not found')
        else:
            childs = page_list.findChildren()
            return len(childs)

    def get_chapter_page(self,chapter_url,page):
        return chapter_url+"/"+str(page)
    
    def get_image_url(self,url):
        soup = Utility.get_soup(url)
        image_div = soup.find('div',{"id": "imgholder"})
        image_url = image_div.find('img')['src']
        return image_url

    def get_chapter_url_to_download(self,url,start,end):
        chapter_url_list = []
        for i in range(int(start),int(end)+1):
            chapter_url_list.append(url+str(i))
        return chapter_url_list

    def download_chapter(self,chapter_url,page_count = 0,folder = None):
        soup = self.get_soup(chapter_url)
        total_page = self.extract_total_page(soup)
        pbar = tqdm(total=total_page,desc=chapter_url)
        image_url_list = []
        download_queue = queue.Queue()
        save_path = self.cwd
        if not folder:
            folder_name = self.extract_title(soup)
            save_path = save_path + '/'+folder_name
            self.prepare_folder(save_path)
            
        for i in range(1,total_page+1):
            page_url = self.get_chapter_page(chapter_url,i)
            download_queue.put(MangaPage(page_url,page_count+i))
        
        for i in range(self.number_of_thread):
            t = BulkImageDownloader(download_queue,save_path,pbar,self.get_image_url)
            t.start()

        download_queue.join()
        pbar.close()
        return page_count+total_page