import requests
import time
import json
import string
from lxml import etree
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_c83ad9c8bbe59cb2528a218a76c83594=1559786443; Hm_lvt_f9b4d143305c6f75248d93b7b5d8f6f1=1559786443; ASP.NET_SessionId=5swi32i0bp2qndkyuiqi3scc; nb-referrer-hostname=www.chacewang.com; currentCity=5a3209b2-f868-47fa-862a-15f5c1f950f4; nb-start-page-url=http%3A%2F%2Fwww.chacewang.com%2FProjectSearch%2FCopyIndex%3Fcitycode%3DRegisterArea_HNDQ_Guangdong_SZ; Hm_lpvt_c83ad9c8bbe59cb2528a218a76c83594=1559913017; Hm_lpvt_f9b4d143305c6f75248d93b7b5d8f6f1=1559913017',
    'Host': 'www.chacewang.com',
    'Referer': 'http://www.chacewang.com/ProjectSearch/CopyIndex?citycode=RegisterArea_HNDQ_Guangdong_SZ',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}

url = 'http://www.chacewang.com/ProjectSearch/FindWithPager?sortField=CreateDateTime&sortOrder=desc&pageindex=0&pageSize=20&cylb=&diqu=RegisterArea_HNDQ_Guangdong_SZ&bumen=&cylbName=&partition=&partitionName=&searchKey=&_=1559913027877'
response = requests.get(url, headers=headers)
resp = response.json()
contents = resp['rows']

font = TTFont('ccw.ttf')
# # font.saveXML('ccw.xml')
uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
chinese_list = [eval(r"u'\u" + uni[3:] + "'") for uni in uni_list[1:] if uni.startswith('uni')]
words_list = [
    '!', '#', '$', '&', '(', ')', '*', '?', '@', '^', '_', '|', '+', '<', '=', '>', 'A', 'a', 'B', 'b', 'C',
    'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm',
    'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X',
    'x', 'Y', 'y', 'Z', 'z', '~', '%', '/', '±'
]
# print(font.getBestCmap())

# word_list = [
#     '9', '8', '3', '4', '7', '5', '&', '>', 'c', 'H', 'q', 'S', '#', 'G', 'h', 'E', 'g', 'x', '(', ')', 'R',
#     '/', 'u', 'r', 'd', '=', 'v', 'j', 'Q', 'V', 'i', 'N', 'B', 'T', '$', 'C', 'n', '!', 'p', 's', 'I', '|', 'L',
#     'F', '%', 'b', '@', 'y', 'Y', '?', '_', 'f', '^', 'Z', 'l', '<', 'a', 'o', 'P', 'm', 't', 'W', 'U', 'O', 'A',
#     'J', 'M', 'e', 'D', 'k', 'z', 'K', 'w', '+', '河', '精', '质', '据', '从', '收', '升', '安', '码', '受', '创',
#     '易', '行', '年', '自', '步', '备', '措', '知', '企', '心', '龙', '因', '集', '限', '及', '列', '配', '专',
#     '贸', '政', '东', '快', '号', '利', '公', '先', '等', '研', '称', '李', '山', '进', '改', '二', '度', '一',
#     '立', '书', '注', '下', '火', '司', '机', '子', '条', '电', '甲', '家', '物', '设', '济', '栋', '助', '励',
#     '天', '策', '小', '五', '光', '当', '有', '乡', '报', '县', '才', '督', '元', '计', '更', '违', '未', '者',
#     '予', '请', '个', '四', '评', '证', '体', '格', '处', '册', '维', '发', '服', '深', '阅', '民', '信', '十',
#     '广', '座', '丙', '云', '中', '任', '首', '华', '单', '道', '保', '万', '事', '新', '项', '与', '询', '术',
#     '提', '件', '股', '扶', '源', '微', '张', '范', '围', '王', '委', '六', '理', '厂', '展', '八', '数', '金',
#     '湖', '属', '罪', '通', '互', '管', '路', '丁', '获', '资', '型', '网', '授', '值', '街', '算', '包', '准',
#     '经', '名', '给', '并', '基', '地', '工', '复', '原', '息', '批', '园', '点', '过', '西', '来', '额', '免',
#     '间', '符', '需', '务', '持', '部', '能', '活', '已', '国', '程', '得', '镇', '或', '域', '总', '水', '再',
#     '的', '括', '时', '市', '验', '合', '文', '拆', '范', '产', '错', '百', '学', '重', '辖', '为', '九', '除',
#     '千', '费', '效', '量', '积', '订', '不', '规', '门', '造', '区', '月', '施', '员', '制', '也', '圳', '七',
#     '还', '省', '联', '位', '北', '建', '革', '南', '监', '查', '字', '究', '阳', '须', '全', '导', '会', '大',
#     '份', '日', '厅', '亿', '环', '法', '贴', '币', '类', '科', '申', '技', '城', '别', '海', '标', '目', '乙',
#     '纸', '主', '三', '优', '图', '所', '商', '州', '刘', '种', '变', '奖', '秀', '补', '京', '高', '人', '运',
#     '2', '1', '6', '*', '~', '±', 'X', '业', '院', '〇', '明', '局', '第'
# ]

num_list = {'4': '9', '5': '8', '6': '3', '7': '4', '8': '7', '9': '5', '1': '2', '2': '1', '3': '6'}

to_chinese_list = [
    '河', '精', '质', '据', '从', '收', '升', '安', '码', '受', '创', '易', '行', '年', '自', '步', '备', '措',
    '知', '企', '心', '龙', '因', '集', '限', '及', '列', '配', '专', '贸', '政', '东', '快', '号', '利', '公',
    '先', '等', '研', '称', '李', '山', '进', '改', '二', '度', '一', '立', '书', '注', '下', '火', '司', '机',
    '子', '条', '电', '甲', '家', '物', '设', '济', '栋', '助', '励', '天', '策', '小', '五', '光', '当', '有',
    '乡', '报', '县', '才', '督', '元', '计', '更', '违', '未', '者', '予', '请', '个', '四', '评', '证', '体',
    '格', '处', '册', '维', '发', '服', '深', '阅', '民', '信', '十', '广', '座', '丙', '云', '中', '任', '首',
    '华', '单', '道', '保', '万', '事', '新', '项', '与', '询', '术', '提', '件', '股', '扶', '源', '微', '张',
    '范', '围', '王', '委', '六', '理', '厂', '展', '八', '数', '金', '湖', '属', '罪', '通', '互', '管', '路',
    '丁', '获', '资', '型', '网', '授', '值', '街', '算', '包', '准', '经', '名', '给', '并', '基', '地', '工',
    '复', '原', '息', '批', '园', '点', '过', '西', '来', '额', '免', '间', '符', '需', '务', '持', '部', '能',
    '活', '已', '国', '程', '得', '镇', '或', '域', '总', '水', '再', '的', '括', '时', '市', '验', '合', '文',
    '拆', '范', '产', '错', '百', '学', '重', '辖', '为', '九', '除', '千', '费', '效', '量', '积', '订', '不',
    '规', '门', '造', '区', '月', '施', '员', '制', '也', '圳', '七', '还', '省', '联', '位', '北', '建', '革',
    '南', '监', '查', '字', '究', '阳', '须', '全', '导', '会', '大', '份', '日', '厅', '亿', '环', '法', '贴',
    '币', '类', '科', '申', '技', '城', '别', '海', '标', '目', '乙', '纸', '主', '三', '优', '图', '所', '商',
    '州', '刘', '种', '变', '奖', '秀', '补', '京', '高', '人', '运', '业', '院', '〇', '明', '局', '第'
]

to_words_list = [
    '&', '>', 'c', 'H', 'q', 'S', '#', 'G', 'h', 'E', 'g', 'x', '(', ')', 'R', '/', 'u', 'r', 'd', '=', 'v',
    'j', 'Q', 'V', 'i', 'N', 'B', 'T', '$', 'C', 'n', '!', 'p', 's', 'I', '|', 'L', 'F', '%', 'b', '@', 'y',
    'Y', '?', '_', 'f', '^', 'Z', 'l', '<', 'a', 'o', 'P', 'm', 't', 'W', 'U', 'O', 'A', 'J', 'M', 'e', 'D',
    'k', 'z', 'K', 'w', '+', '*', '~', '±', 'X'
]

chinese = dict(zip(chinese_list, to_chinese_list))
words = dict(zip(words_list, to_words_list))

chinese.update(words)
# print(chinese)
def transform(data: str, turn_word: dict):
    ans = ''
    for i in data:
        ans += turn_word[i] if i in turn_word else i
    data = ans
    return data


for content in contents:
    # ans = ''
    # for i in content['PEName']:
    #     ans += word[i] if i in utf8_list else i
    # content['PEName'], ans = ans, ''
    content['PEName'] = transform(content['PEName'], chinese)
    print(content['PEName'])

    # for i in content['AreaFullName']:
    #     ans += word[i] if i in utf8_list else i
    # content['AreaFullName'], ans = ans, ''
    content['AreaFullName'] = transform(content['AreaFullName'], chinese)
    print(content['AreaFullName'])

    # for i in content['DeptFullName']:
    #     ans += word[i] if i in utf8_list else i
    # content['DeptFullName'], ans = ans, ''
    content['DeptFullName'] = transform(content['DeptFullName'], chinese)
    print(content['DeptFullName'])

    # for val in content['SETime']:
    #     ans += num_list[val] if val in num_list else val
    # content['SETime'] = ans
    content['SETime'] = transform(content['SETime'], num_list)
    print(content['SETime'])

    content['Partition'] = transform(content['Partition'], words)
    print(content['Partition'])

    main_id = content['MainID']
    detail_url = 'http://www.chacewang.com/ProjectSearch/PeDetail/{}?from=home'.format(main_id)
    rsp = requests.get(detail_url, headers=headers)
    print(rsp.text)
    time.sleep(2)