from info_downloader import VideoInfoDownloader
from subtitle_downloader import SubtitleDownloader
from writein import writein
    
import argparse
import os
class NoArgsError:
    pass

def read_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bv", help = "获取bv号")
    parser.add_argument("-p", help = "分p，默认为0")
    args = parser.parse_args()
    return (args.bv, args.p)
def main():
    # with open("settings.json", "r") as f:
    #     settings = json.load(f)
    # notion_token = settings.get("notion_token")
    # database_id = settings.get("database_id")
    # api_key = settings.get("api_key")
    
    cookie = None
    if os.path.isfile("./cookie"):
        with open("./cookie", "r") as f:
            cookie = f.read()
            
    bvid, p = read_command_line_args()
    bvid = bvid if bvid is not None else input("请输入bvid:")
    p_num = p if p is not None else 0
    
    print(f"正在获取{bvid}的视频信息...")
    video_info = VideoInfoDownloader(bvid, cookie).download_info()
    title = video_info['info']['title']
    print(f"视频标题：{title}")
    subtitle = SubtitleDownloader(bvid, p_num, cookie).download_subtitle()
    print("字幕获取成功")
    writein(title, subtitle)
    print("写入成功")
    
if __name__ == '__main__':
    main()