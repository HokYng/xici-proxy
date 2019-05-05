from mitmproxy.http import HTTPFlow
from mitmproxy import ctx
import json
import os


class DouYin:
    def __init__(self):
        self.path = 'D:\Viedio'
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        else:
            for i in os.listdir(self.path):
                s = os.path.join(self.path, i)
                os.remove(s)

    def response(self, flow:HTTPFlow):
        url_pre = 'https://aweme-eagle-hl.snssdk.com/aweme/v1/feed/'
        if flow.request.url.startswith(url_pre):
            data = json.loads(flow.response.text)
            try:
                for item in data['aweme_list']:
                    title = item['desc']
                    author = item['author']['nickname']
                    author_id = item['author']['unique_id']
                    vedio = item['video']['play_addr_265']['url_list'][0]
                    res = requests.get(vedio, stream=True, verify=False)
                    filename = os.path.join(self.path, '{}.mp4'.format(title))
                    with open(filename, 'wb') as f:
                        for v in res.iter_content(chunk_size=1024):
                            f.write(v)
            except KeyError as e:
                ctx.log.error(e)


addons = [DouYin()]