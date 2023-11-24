from info_downloader.info_downloader import VideoInfoDownloader
from subtitle_downloader.subtitle_downloader import SubtitleDownloader

def writein(video_info, subtitle):
    with open(f"{video_info['info']['title']}.md", "w") as f:
        f.write(f"# {video_info['info']['title']}\n")
        f.write(f"![cover]({video_info['info']['pic']})\n")
        f.write(subtitle)