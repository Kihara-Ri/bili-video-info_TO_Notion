import requests
from info_downloader.section_info import section_dict

class VideoInfoDownloader:
    def __init__(self, bvid: str, cookie: str) -> None:
       self.bvid = bvid
       self.info_api = "https://api.bilibili.com/x/web-interface/view"
       self.tags_api = "https://api.bilibili.com/x/web-interface/view/detail/tag"
       self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'cookie': cookie,
        }
    def _get_info(self):
        params = (
            ("bvid", self.bvid),
        )
        response = requests.get(self.info_api, params=params, headers = self.headers)
        return response.json()['data']
    
    def _get_tags(self):
        params = (
            ("bvid", self.bvid),
        )
        response = requests.get(self.tags_api, params=params, headers = self.headers)
        try:
            data = response.json()['data'] # 报错: KeyError: 'data'
            if data:
                tags = [x['tag_name'] for x in data]
                if len(tags) > 5:
                    tags = tags[:5]
            else:
                tags = []
            return tags
        except Exception as e:
            print(f"获取tag信息失败，bvid: {self.bvid}")
            return []
    
    def download_info(self):
        info = self._get_info()
        tags = self._get_tags()
        # print(info['tid'])
        try:
            section = section_dict[info['tid']]
            # print(section)
        except Exception as e:
            print(f"目前暂无分区信息，tid: {info['tid']}")
            section = section_dict[229] # 没有分区信息就默认归类知识区
            
        return {
            "info": info,
            "tags": tags,
            "section": section,
            "bvid": self.bvid
        }