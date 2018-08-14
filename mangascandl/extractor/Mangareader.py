from .common import MangaSiteExtractor
from .common import MangaUrlError
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

   def get_image_url(self,soup):
       image_div = soup.find('div',{"id": "imgholder"})
       image_url = image_div.find('img')['src']
       return image_url
