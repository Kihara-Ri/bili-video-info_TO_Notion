import requests
import os
import subprocess


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
        # print(response.json())
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            return ['https:' + x['subtitle_url'] for x in subtitles]
        return []
    
    def _get_subtitle(self, cid: str):
        subtitles = self._get_subtitle_list(cid)
        if subtitles:
            return self._request_subtitle(subtitles[0])
        else:
            cookie_path = find_path("cookie")
            with open(f"{cookie_path}", "r") as f:
                cookie = f.read().strip() # 去除换行符
            print(f"旧cookie: {cookie}")
            input("cookie已失效，请输入新的cookie (space)...")
            edit_cookie_with_vim()
            
            with open(f"{cookie_path}", "r") as f:
                print("正在读取新的cookie...")
                cookie = f.read().strip()
            self.headers['cookie'] = cookie
            subtitles = self._get_subtitle_list(cid)
            print("新cookie读取成功！")
            if subtitles:
                return self._request_subtitle(subtitles[0])
            else:
                print(f"视频 https://bilibili.com/video/{self.bvid}/ 没有cc字幕")
                return None
            
        # raise SubtitleDownloadError(f"下载失败，请检查该视频是否有cc字幕")
    
    def _request_subtitle(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()['body']
            return body
        
    def download_subtitle(self):
        cookie_path = find_path("cookie")
        with open(f"{cookie_path}", "r") as f:
            cookie = f.read().strip() # 去除换行符
        self.headers['cookie'] = cookie
        subtitle_list = self._get_subtitle(self._get_player_list()[self.p_num])
        if subtitle_list:
            text_list = [x['content'] for x in subtitle_list]
            text = '，'.join(text_list)
            return text
        else:
            text = "该视频没有字幕"
            return text
    
class SubtitleDownloadError(Exception):
    pass


def edit_cookie_with_vim():
    cookie_path = find_path("cookie")
    try:
        if not os.path.exists(cookie_path):
            with open(cookie_path, "w") as fp:
                pass
            
        # 调用shell脚本来编辑cookie
        subprocess.run(["vim", cookie_path], check = True)
    except subprocess.CalledProcessError:
        print("vim编辑cookie失败，请手动编辑cookie文件")
    except Exception as e:
        print(f"发生错误: {e}")
    
def find_path(file_name):
    main_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(main_dir, file_name)
    return file_path