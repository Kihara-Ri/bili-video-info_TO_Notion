import requests

# 加上请求头，否则经常报错412
cookie = "buvid3=5469CAA4-3327-6817-C110-63EC4C48A2B841595infoc; b_nut=1690905941; i-wanna-go-back=-1; _uuid=D12D3DD8-A212-6C5D-B11C-B981056FBDBAC42037infoc; FEED_LIVE_VERSION=V8; DedeUserID=631081975; DedeUserID__ckMd5=8480d8688fb0d91c; CURRENT_FNVAL=4048; buvid4=F5C72193-655E-A103-CF78-0D472A9B9E7042640-023080200-S1vCeaCWwH6m%2B4KHu4XUBQ%3D%3D; hit-new-style-dyn=1; hit-dyn-v2=1; header_theme_version=CLOSE; home_feed_column=5; rpdid=|(kmJYkYmJJJ0J'uYmuJmJkY); b_ut=5; CURRENT_QUALITY=112; enable_web_push=DISABLE; bsource=search_google; bp_article_offset_631081975=859991180132221012; fingerprint=31cedae465023077a9a68974b5b29f04; buvid_fp_plain=undefined; buvid_fp=31cedae465023077a9a68974b5b29f04; browser_resolution=1800-1008; PVID=5; SESSDATA=ae3a8f54%2C1716175064%2Ce3e49%2Ab2CjBHKHEYjbEDIXilb6TpFZ3DRt6ayI8zxe6UlDTZpfGEbVlu1ugKGCeEDweifDiUFW4SVlp5UHczVHJibVI0OTdHMFc4TXdraVlONEZ5aWN6VkJjOXowNnZjWGxiQ3hnUW5ZSWpwaVUwRDhub09kODRZMlBsaTVibmFxd2R5M1c5b2EwMGhtbmlnIIEC; bili_jct=3208e9e6aa22067a9cf8d8541e23c6ed; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDA4ODIyNzgsImlhdCI6MTcwMDYyMzAxOCwicGx0IjotMX0.Pn4xgTW_mv5zcX480n5RZ8WXGPRLuB02VuKNDSjAOi0; bili_ticket_expires=1700882218; sid=4t2204gr; b_lsid=975D43E5_18BF6F0CE4A; bp_video_offset_631081975=866793235808256086"
headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'cookie': cookie
    }

def bili_info(bvid):
    
    params = (
        ('bvid', bvid),
    )
    response = requests.get('https://api.bilibili.com/x/web-interface/view', params = params, headers = headers)
    # 为了防止报错了不知道，还是加上为好
    if response.status_code == 200:
        return response.json()['data']
    else:
        print('访问出错:')
        return response
def bili_tags(bvid):
    params = (
        ('bvid', bvid),
    )

    response = requests.get('https://api.bilibili.com/x/web-interface/view/detail/tag', params=params)
    data = response.json()['data']
    if data:
        tags = [x['tag_name'] for x in data]
        if len(tags) > 5:
            tags = tags[:5]
    else:
        tags = []
    return tags

    
# print('标题：', data['title'])
# print('up主：', data['owner']['name'])
# print('播放量：', data['stat']['view'])

data = bili_info(bvid)
print('标题：', data.get('title', 'N/A'))
print('up主：', data['owner'].get('name', 'N/A'))
print('播放量：', data['stat'].get('view', 'N/A'))

tags = bili_tags(bvid)
print(tags)

# 这里是对视频cid的获取
def bili_player_list(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid='+bvid
    response = requests.get(url, headers = headers)
    # 获取cid
    cid_list = response.json()['data'][0].get('cid')
    return cid_list

def bili_subtitle_list(bvid, cid):
    url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
    response = requests.get(url, headers = headers)
    returnjson = response.json()
    # 这里的subtitles中储存了字幕的url，用该url来访问字幕json文件
    subtitles = response.json()['data']['subtitle']['subtitles']
    # 如果有字幕的，则返回这些有字幕的链接，否则返回空，没有说明cookie不对或者根本就没有AI字幕，大概率是前者
    # 注意下面subtitles为list型变量，不能使用get方法
    if subtitles:
        return ['https:' + x['subtitle_url'] for x in subtitles]
    else:
        return []
    
    
def bili_subtitle(bvid, cid):
    # add cookies if necessary
    # 注意这里的subtitles数组中存放的是视频的url
    subtitles = bili_subtitle_list(bvid, cid)
    if subtitles:
        response = requests.get(subtitles[0], headers=headers)
        if response.status_code == 200:
            body = response.json()['body']
            return body
        else:
            print("请求错误：")
            return response.status_code
    return []

subtitle_text = bili_subtitle(bvid, bili_player_list(bvid))
subtitle_text

text_list = [x['content'] for x in subtitle_text]
text_list

text = '，'.join(text_list)
text

with open(f"{data.get('title')}.md", "w") as f:
   f.write(text)