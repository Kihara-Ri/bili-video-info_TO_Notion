from info_downloader import VideoInfoDownloader
from subtitle_downloader import SubtitleDownloader
from GPT_summary import GPT_summary
from submit_to_notion import submit_to_notion
from writein import writein
    
import argparse
import json
import os

class NoArgsError:
    pass

def read_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bv", help = "获取bv号")
    parser.add_argument("-p", help = "分p，默认为0")
    parser.add_argument("--summary_count", help="需要的精简概括的数量（默认为10条）")
    args = parser.parse_args()
    return (args.bv, args.p, args.summary_count)

def main():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    notion_token = settings.get("notion_token")
    database_id = settings.get("database_id")
    api_key = settings.get("api_key")
    
    cookie = None
    if os.path.isfile("./cookie"):
        with open("./cookie", "r") as f:
            cookie = f.read()
            
    bvid, p, summary_count = read_command_line_args()
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
    
    # summary = GPT_summary(api_key, subtitle, summary_count).write_summary()
    # print("chatGPT编写摘要成功")
    submit_to_notion(notion_token, database_id).insert_to_notion(video_info, subtitle)
    print("导入Notion成功")
    
if __name__ == '__main__':
    main()