# -*- coding: utf-8 -*-
import re


# 仲裁文书跟行政处罚类型，处罚机关匹配规则
def get_real_cf_xzjg(txt):
    if txt:
        while True:
            data = re.findall(r'[。）： ](.*?(?:部|厅|局|会|院|政府|队|处|处罚中心|中国南方电网有限责任公司|互联网金融平台))', txt)
            if data:
                data = data[-1]
            else:
                data = ''
            if "。" in data or "）" in data or "：" in data or ' ' in data:
                txt = data
            else:
                return data
    else:
        return ''


if __name__ == '__main__':
    txt = '徐文生：秦皇岛市九正房地产开发有限公司单位法定代表人:徐文生(身份证号码：130302196610211119)。根据《中华人民共和国行政强制法》第三十五条和第五十四条之规定，限你（单位）于2019年2月6日前履行公安机关于2018年8月22日作出的给予山海国际商业、居住小区A、B标段责令停止使用，并处罚款人民币陆万元整的行政决定，决定书文号为:秦山公（消）行罚决字（2018）0015号。持决定书到中国工商银行股份有限公司秦皇岛山海关支行（地址：山海关区南海西路）缴纳滞纳金陆万元整。对以上事项，你（单位）有权进行陈述和申辩，无正当理由逾期不履行的，将依法强制执行。秦皇岛市山海关区公安消防大队'
    result = get_real_cf_xzjg(txt)
    print(result)