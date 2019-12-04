# -*- coding: utf-8 -*-
keywords = [
    {'kind_id': '0', 'cflb': '公告类型'},
    {'kind_id': '1', 'cflb': '起诉状、上诉状副本'},
    {'kind_id': '2', 'cflb': '开庭传票'},
    {'kind_id': '3', 'cflb': '裁判文书'},
    {'kind_id': '4', 'cflb': '公示催告'},
    {'kind_id': '5', 'cflb': '破产文书'},
    {'kind_id': '6', 'cflb': '宣告失踪、死亡'},
    {'kind_id': '7', 'cflb': '执行文书'},
    {'kind_id': '8', 'cflb': '无主财产认领公告'},
    {'kind_id': '9', 'cflb': '起诉状副本及开庭传票'},
    {'kind_id': '10', 'cflb': '其他'},
    {'kind_id': '11', 'cflb': '更正'},
    {'kind_id': '12', 'cflb': '遗失声明'},
    {'kind_id': '13', 'cflb': '司法鉴定书'},
    {'kind_id': '14', 'cflb': '海事文书'},
    {'kind_id': '15', 'cflb': '仲裁文书'},
    {'kind_id': '16', 'cflb': '拍卖公告'},
    {'kind_id': '17', 'cflb': '清算公告'},
    {'kind_id': '18', 'cflb': '行政处罚通知书'},
    {'kind_id': '19', 'cflb': '版权公告'},
    {'kind_id': '20', 'cflb': '公益诉讼'},
]


def keyword_generator():
    for keyword in keywords:
        kind_id = keyword.get('kind_id')
        yield kind_id


import datetime
if __name__ == '__main__':
    results = keyword_generator()
    for a in results:
        print(a)
    # today = datetime.datetime.now().strftime("%Y-%m-%d")
    # print(today)