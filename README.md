<div align="center">
  <img src="bili_notion.svg" alt="img" title=" alt=&quot;background copy&quot; style=&quot;" style="zoom: 50%;" width="50%" height="50%"/> 
</div>
## 快速上手

请根据下面的命令安装依赖库

```shell
pip install oss2
pip install requests
```

本项目包括两个部分

### b站的API请求

使用的API有：

- ‘https://api.bilibili.com/x/web-interface/view’ ，带参数`bvid`
- 'https://api.bilibili.com/x/player/pagelist?bvid=' +bvid，用于请求`cid`
- f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}' ，用于请求`subtitle_url`
- 返回的`subtitle_url`，用于获取字幕

详细抓取过程请见jupyter notebook

### 目录

```shell
$ tree
.
├── GPT_API.ipynb
├── GUI # 将会尝试添加图形界面
│   └── GUI.py
├── README.md
├── bilibili_API.ipynb
└── workflow
    ├── GPT_summary # 由于各种原因GPT的部分暂时不使用，将会尝试用b站的视频助手
    │   ├── GPT_summary.py
    │   ├── __init__.py
    │   └── __pycache__
    ├── bilidl
    ├── info_downloader
    │   ├── __init__.py
    │   ├── info_downloader.py
    │   └── section_info.py
    ├── main.py
    ├── settings.json # 里面存放的都是敏感信息，请手动添加此文件
    ├── submit_to_notion
    │   ├── __init__.py
    │   └── submit_to_notion.py
    ├── subtitle_downloader
    │   ├── __init__.py
    │   ├── cookie # 可以不添加，命令会提示使用vim添加
    │   └── subtitle_downloader.py
    └── writein.py
```

### 程序运行工作流

1. 命令行获取参数`bvid`，`p_num`
2. 从程序相对目录下获取`cookie`，如果`cookie`失效，则提示使用`vim`写入`cookie`
3. 从`settings.json`中读取`notion`和`aliyun oss`的`id`和密钥等信息
4. 访问b站API
   1. `bili_info`, `bili_tags`
   2. `subtitle_downloader`
5. 视频`cover`上传至阿里云图床（后续本地markdown文件和notion中的cover都将使用阿里云图床的url）
6. 读取的`subtitles`写入markdown文件，文件将默认保存在执行目录下
7. 上传至`notion`数据库

## workflow
---
自动化流程：

```mermaid
graph LR
prompt(prompt)
para((bvid, p_num))
judge{if cookie is valid ?}
write(write in with vim)
read(settings.json)
check((check subtitles))
requests(bilibili API)
upload(upload cover)
import((import to notion))

prompt --> judge
para --> judge
judge --> |Yes| read
judge --> |No | write
write --> judge2{if cookie is valid ?}
judge2 --> |Yes| read
judge2 --> |No| check
read --> requests
requests --> upload
upload --> import
```
---


b站API的请求原理图：

```mermaid
graph TD

get{requests}

info(bili_info)
tags(bili_tags)
cid(cid)
bvid(bvid)
json_api(json_api)
subtitle_url(subtitle_url)
information((information))
subtitle_json((subtitle_json))

bvid --> get
get -.-> info
get -.-> tags

info --> information
tags --> information

get -.-> cid
bid(bvid) -.-> json_api
cid --> json_api
json_api --> subtitle_url
subtitle_url --> subtitle_json
```

---

## 需要做的准备

### 关联数据库

在`Notion`中创建数据库，保存密钥


本地创建database

格式如下：

| NAME     | TYPE            |
| -------- | --------------- |
| title    | `title`         |
| cover    | `files & media` |
| URL      | `URL`           |
| UP主     | `text`          |
| 分区     | `select`        |
| tags     | `multi select`  |
| 发布时间 | `date`          |
| 加入时间 | `date`          |

得到`notion_token`和`database_id`

### 上传至图床

本项目从bilibili获取的`cover`将会上传至阿里云oss图床中

markdown文本和上传至notion中的图片链接均为阿里云图床的链接

得到`access_key_id`，`access-key-secret`，`bucket_name`和`endpoint`

### 添加密钥

在`workflow`目录下添加`settings.json`文件，内容如下：

```json
{
    "notion_token": "",
    "database_id": "",
    "api_key": "",
    "access_key_id": "",
    "access_key_secret": "",
    "bucket_name": "",
    "endpoint": ""
}
```

将之前得到的信息填入对应的键值对中即OK

`api_key`为chatGPT的API密钥，目前功能还不完整因此不要填

### shell

为程序添加了命令行访问的方法，实现了在任何目录下使用该命令

shell脚本的文件名：`bilidl`，可以没有`.sh`后缀

```shell
#!/bin/bash

if [ "$#" -eq 1 ]; then
    python /path/to/main.py "$1"
elif [ "$#" -eq 2 ] && [ "$2" = "p_num" ]; then
    python /path/to/main.py "$1" p_num
else
    echo "Usage: bilidl.sh bvid [p_num]"
    exit 1
fi
```

你需要将`main.py`文件的绝对地址 `/path/to/main.py`改为在你的计算机中的绝对地址

给予执行权限：

```shel
chmod +x bilidl
```

移动到系统的PATH（添加到环境变量）中：

```shell
sudo mv bilidl /usr/local/bin
```

在执行时使用如下命令：

```shell
bilidl <bvid> (p_num)
```

`p_num`是可有可无的，无参数时默认为`0`

## 试例

![Screenshot 2023-11-29 at 21.45.05](https://mdstore.oss-cn-beijing.aliyuncs.com/Screenshot%202023-11-29%20at%2021.45.05.png)



![Screenshot 2023-12-11 at 19.56.05](https://mdstore.oss-cn-beijing.aliyuncs.com/markdown/Screenshot%202023-12-11%20at%2019.56.05.png)



![Screenshot 2023-12-11 at 20.26.47](https://mdstore.oss-cn-beijing.aliyuncs.com/markdown/Screenshot%202023-12-11%20at%2020.26.47.png)



![Screenshot 2023-12-11 at 20.27.14](https://mdstore.oss-cn-beijing.aliyuncs.com/markdown/Screenshot%202023-12-11%20at%2020.27.14.png)

## References

- https://developers.notion.com/reference/intro

- https://github.com/DavinciEvans/chatGPT-Summary-Bilibili-To-Notion

- https://zhuanlan.zhihu.com/p/610250035
