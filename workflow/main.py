from info_downloader import VideoInfoDownloader
from subtitle_downloader import SubtitleDownloader
# from GPT_summary import GPT_summary
from submit_to_notion import submit_to_notion
from writein import writein
import time
    
import argparse
import json
import os
import sys

class NoArgsError:
    pass

def read_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bvid", help = "获取bvid")
    parser.add_argument("-p_num", help = "分p数，默认为0")
    # parser.add_argument("--summary_count", help="需要的精简概括的数量（默认为10条）")
    args = parser.parse_args()
    return (args.bv, 
            args.p_num, 
            # args.summary_count
            )
    
def find_path(file_name):
    main_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(main_dir, file_name)
    return file_path

def main():
    settings_path = find_path("settings.json")
    cookie_path = find_path("cookie")
    with open(f"{settings_path}", "r") as f:
        settings = json.load(f)
    notion_token = settings.get("notion_token")
    database_id = settings.get("database_id")
    access_key_id = settings.get("access_key_id")
    access_key_secret = settings.get("access_key_secret")
    bucket_name = settings.get("bucket_name")
    endpoint = settings.get("endpoint")
    # api_key = settings.get("api_key")
    
    cookie = None
    if os.path.isfile(f"{cookie_path}"):
        with open(f"{cookie_path}", "r") as f:
            cookie = f.read()
            
    # 命令行传参 bvid, p, chatGPT总结信息，目前不需要总结已去除
    # bvid, p_num, = read_command_line_args()
    # bvid = bvid if bvid is not None else input("请输入bvid:")
    # p_num = p_num if p_num is not None else 0
    
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("参数错误，请输入正确的参数")
        sys.exit(1)
        
    bvid = sys.argv[1]
    p_num = int(sys.argv[2]) if len(sys.argv) == 4 and sys.argv[2] == "p_num" else 0
    
    print(f"正在获取{bvid}的视频信息...")
    video_info = VideoInfoDownloader(bvid, cookie).download_info()
    title = video_info['info']['title']
    print(f"视频标题: {title}")
    print(f"cover: {video_info['info']['pic']}")
    print(f"up主: {video_info['info']['owner']['name']}")
    print(f"发布时间: {time.strftime('%Y-%m-%d', time.localtime(video_info['info']['pubdate']))}")
    print(f"标签: {video_info['tags']}")
    
    subtitle = SubtitleDownloader(bvid, p_num, cookie).download_subtitle()
    print("字幕获取成功")
    remote_file_path = writein(video_info, subtitle, cookie, access_key_id, access_key_secret, bucket_name, endpoint)
    print("写入成功")


    
    # summary = GPT_summary(api_key, subtitle, summary_count).write_summary()
    # print("chatGPT编写摘要成功")
    summary = video_info['info']['dynamic']
    # print("summary : ", summary)
    submit_to_notion(notion_token, database_id).insert_to_notion(video_info, summary, subtitle, remote_file_path)
    print("导入Notion成功")
    
if __name__ == '__main__':
    main()