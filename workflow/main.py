


def main():
    token = 'your-token'
    database_id = 'your-db-id'
    while True:
        blink = input('请输入B站视频链接：')
        bvid = blink.split('/')[4]
        print(f'开始处理视频信息：{bvid}')
        prompt = '我希望你是一名专业的视频内容编辑，请你尝试修正以下视频字幕文本中的拼写错误后，将其精华内容进行总结，然后以无序列表的方式返回，不要超过5条！确保所有的句子都足够精简，清晰完整。'
        transcript_text = bili_subtitle(bvid, bili_player_list(bvid)[0])
        if transcript_text:
            print('字幕获取成功')
            seged_text = segTranscipt(transcript_text)
            summarized_text = ''
            i = 1
            for entry in seged_text:
                try:
                    response = chat(prompt, entry)
                    print(f'完成第{str(i)}部分摘要')
                    i += 1
                except:
                    print('GPT接口摘要失败, 请检查网络连接')
                    response = '摘要失败'
                summarized_text += '\n'+response
            insert2notion(token, database_id, bvid, summarized_text)
        else:
            print('字幕获取失败\n')

if __name__ == '__main__':
    main()