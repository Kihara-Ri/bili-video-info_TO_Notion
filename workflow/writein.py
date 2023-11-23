from info_downloader import VideoInfoDownloader
from subtitle_downloader import SubtitleDownloader

def writein(title, subtitle):
    with open(f"{title}.md", "w") as f:
        f.write(subtitle)