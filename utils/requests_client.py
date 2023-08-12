from utils.constants import BASE_HEADERS, NEW_LINE
import requests

class RequestsClient(object):
    def __init__(self):
        self.res = None 
    
    def __str__(self):
        info = (f'url: {self.url}',
                f'headers: {self.headers}',
                f'res: {self.res}')

        return NEW_LINE.join(info)

    def request(self, url, headers=BASE_HEADERS):
        try:
            request = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            self.res = request

    @property 
    def content(self):
        return self.res.content.decode("utf-8")

    @property
    def status(self):
        return self.res.status_code

    @property
    def text(self):
        return self.res.text