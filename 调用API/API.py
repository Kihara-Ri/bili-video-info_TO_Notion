import requests

def bili_info(bvid):
    params = (
        ('bvid', bvid),
    )
    response = requests.get('https://api.bilibili.com/x/web-interface/view', params=params)
    return response.json()['data']

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

bvid = "BV1iN411g7zi"
data = bili_info(bvid)

print('标题：', data['title'])
print('up主：', data['owner']['name'])
print('播放量：', data['stat']['view'])