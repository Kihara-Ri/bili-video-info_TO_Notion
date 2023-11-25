import requests
import oss2
from urllib.parse import quote
import os

def writein(video_info, subtitle, cookie, access_key_id, access_key_secret, bucket_name, endpoint):
    headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'cookie': cookie,
        }
    cover_url = video_info['info']['pic']
    title = video_info['info']['title']
    # 将汉字编译为utf-8
    cover_name = f"{quote(title, safe='')}.jpg"
    cover = requests.get(cover_url, headers = headers).content
    # 下载cover到本地
    with open(f"{cover_name}", 'wb') as f:
        f.write(cover)
        f.close()
    # 本地markdown
    with open(f"{title}.md", "w") as f:
        f.write(f"# {title}\n")
        remote_file_path = upload_to_aliyun(cover_name, access_key_id, access_key_secret, bucket_name, endpoint)
        f.write(f"![{title}.jpg]({remote_file_path})\n")
        f.write(subtitle)
        
    return remote_file_path
        
def upload_to_aliyun(local_file_path, access_key_id, access_key_secret, bucket_name, endpoint,oss_folder = ''):
    # 远程文件路径
    if oss_folder:
        remote_file_path = f'{oss_folder}/{local_file_path}'
    else:
        remote_file_path = local_file_path
        
    # 创建存储空间实例
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 上传图片
    try:
        bucket.put_object_from_file(remote_file_path, local_file_path)
        # 这里要注意url对%的编码，否则得到的本地文件名与图床中的不一致，被再次编码
        remote_file_path = f"https://{bucket_name}.{endpoint}/{quote(remote_file_path)}"
        print(f'Image uploaded successfully! Access URL: {remote_file_path}')
        # 删除本地图片
        os.remove(local_file_path)
        # return f"{os.getcwd()}/workflow/{local_file_path}"
        return remote_file_path
    except oss2.exceptions.OssError as e:
        print(f'文件上传失败: {e}')
        return None