import requests
import os

class SubtitleDownloader:
    def __init__(self, bvid: str, p_num, cookie: str):
        self.bvid = bvid
        self.p_num = p_num
        self.pagelist_api = "https://api.bilibili.com/x/player/pagelist"
        self.subtitle_api = "https://api.bilibili.com/x/player/v2"
        self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'cookie': cookie,
        }
        
    def _get_player_list(self):
        response = requests.get(self.pagelist_api, params = {'bvid': self.bvid}, headers = self.headers)
        cid_list = [x['cid'] for x in response.json()['data']]
        return cid_list
    
    def _get_subtitle_list(self, cid: str):
        params = (
            ('bvid', self.bvid),
            ('cid', cid),
        )
        response = requests.get(self.subtitle_api, params = params, headers = self.headers)
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            return ['https:' + x['subtitle_url'] for x in subtitles]
        return []
    
    def _get_subtitle(self, cid: str):
        subtitles = self._get_subtitle_list(cid)
        if subtitles:
            return self._request_subtitle(subtitles[0])
        else:
            cookie = input("cookie已失效，请输入新的cookie：")
            with open("./cookie", "w") as f:
                f.write(cookie)
            self.headers['cookie'] = cookie
            subtitles = self._get_subtitle_list(cid)
            if subtitles:
                return self._request_subtitle(subtitles[0])
            
        raise SubtitleDownloadError("下载失败，cookie已失效，请更换新的cookie")
    
    def _request_subtitle(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()['body']
            return body
        
    def download_subtitle(self):
        subtitle_list = self._get_subtitle(self._get_player_list()[self.p_num])
        text_list = [x['content'] for x in subtitle_list]
        text = '，'.join(text_list)
        return text
    
class SubtitleDownloadError(Exception):
    pass