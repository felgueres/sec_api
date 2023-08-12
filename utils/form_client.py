from requests_client import RequestsClient
from utils import is_html_tag_visible
import bs4 as bs

class FormClient(object):

    def __init__(self, url):
        self.url = url
        self.client = RequestsClient()
        self.soup = None

    def fetch_text_from_url(self):
        print('Requesting {} ... '.format(self.url))
        self.client.request(self.url)
        print('Request Status: {}'.format(self.client.status))
        self.soup = bs.BeautifulSoup(self.client.text, 'lxml') 
        return self

    def get_text(self):
        texts = self.soup.findAll(text=True)
        texts = filter(is_html_tag_visible, texts)
        return list(texts)