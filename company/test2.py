# import re
# import requests
# from lxml import etree
# from fontTools.ttLib import TTFont
#
# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 "
#               "Safari/537.36 "
# }
#
# url = 'https://club.autohome.com.cn/bbs/thread/1d0784305887ec3f/72381110-1.html#pvareaid=102410'
#
# # 请求内容
# response = requests.get(url, headers=headers)
# response_html = response.content.decode('gbk')
# # print(response_html)
# # xpath 获取帖子内容
# response_xml = etree.HTML(response_html)
# content_list = response_xml.xpath('//div[@xname="content"]//div[@class="tz-paragraph"]//text()')
# content_str = ''.join(content_list)
#
# # 获取字体的连接文件
# fonts_ = re.search(r",url\('(//.*\.ttf)?'\) format", response_html).group(1)
#
# # 请求字体文件， 字体文件是动态更新的
# fonts_url = 'https:'+fonts_
# response = requests.get(fonts_url, headers=headers).content
# # 讲字体文件保存到本地
# with open('fonts.ttf', 'wb') as f:
#     f.write(response)
#
# # 解析字体库
# font = TTFont('fonts.ttf')
#
# # 读取字体的映射关系
# uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
#
# # 转换格式
# utf_list = [eval(r"u'\u" + x[3:] + "'") for x in uni_list[1:]]
#
# # 被替换的字体的列表
# word_list = [u'六', u'近', u'二', u'元', u'五', u'是', u'九', u'了', u'着', u'左', u'更', u'呢', u'下',
#          u'七', u'四', u'坏', u'八', u'大', u'十', u'一', u'多', u'短', u'少', u'三', u'又',
#          u'不', u'地', u'很', u'长', u'小', u'和', u'上', u'得', u'矮', u'低', u'好', u'的', u'高']
# #遍历需要被替换的字符
# for i in range(len(utf_list)):
#     content_str = content_str.replace(utf_list[i], word_list[i])
# print(content_str)


import re
import requests
from fontTools.ttLib import TTFont
from lxml import etree

headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/66.0.3359.139 Safari/537.36 "
    }

index_url = 'http://maoyan.com/'
# 获取首页内容
response_index = requests.get(index_url, headers=headers).text
index_xml = etree.HTML(response_index)
info_list = index_xml.xpath('//*[@id="app"]/div/div[1]/div[1]/div/div[2]/ul/li[1]/a/div[2]/div//text()')
a = u'电影名称：%s, 票房总数：%s' % (info_list[1], info_list[4])
print (a)

# 获取字体文件的url
woff_ = re.search(r"url\('(.*\.woff)'\)", response_index).group(1)
woff_url = 'http:' + woff_
response_woff = requests.get(woff_url, headers=headers).content

with open('fonts.woff', 'wb') as f:
    f.write(response_woff)

#base_nums， base_fonts 需要自己手动解析映射关系， 要和basefonts.woff一致
baseFonts = TTFont('basefonts.woff')
base_nums = ['7', '9', '8', '5', '1', '6', '4', '0', '2', '3']
base_fonts = ['uniE1BF', 'uniEBD6', 'uniF806', 'uniE983', 'uniF386', 'uniF2A2', 'uniE05B', 'uniE8C8', 'uniE032',
              'uniF67D']
onlineFonts = TTFont('fonts.woff')

# onlineFonts.saveXML('test.xml')

uni_list = onlineFonts.getGlyphNames()[1:-1]
temp = {}
# 解析字体库
for i in range(10):
    onlineGlyph = onlineFonts['glyf'][uni_list[i]]
    for j in range(10):
        baseGlyph = baseFonts['glyf'][base_fonts[j]]
        if onlineGlyph == baseGlyph:
            temp["&#x" + uni_list[i][3:].lower() + ';'] = base_nums[j]

# 字符替换
pat = '(' + '|'.join(temp.keys()) + ')'
response_index = re.sub(pat, lambda x: temp[x.group()],     response_index)

# 内容提取
index_xml = etree.HTML(response_index)
info_list = index_xml.xpath('//*[@id="app"]/div/div[1]/div[1]        /div/div[2]/ul/li[1]/a/div[2]/div//text()')
a = u'电影名称：%s, 票房总数：%s' % (info_list[1], info_list[4])
print(a)