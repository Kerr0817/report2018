# -*- coding: utf-8 -*-
# 字体库
from reportlab.pdfgen.canvas import Canvas
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import os
# 字体
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# 用于定位的inch库，inch将作为我们的高度宽度的单位
from reportlab.lib.units import inch
# 颜色
from reportlab.lib.colors import HexColor
# 时间戳
from datetime import datetime
# 热词
import jieba
from collections import Counter
# 词云
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# 遮罩
from PIL import Image


def create_pdf(
               friend_hotwords_image='./image/we2.png',
               name='李爱国国',                                            # 用户名
               name_id='111111199312091111',                               # 用户id√
               head_image='./image/我.png',                                # 头像
               key_words='硬核少年',                                       # 关键词
               user_data=[0.1993, 0.1993, 0.1993, 0.1993, 0.1993, 0.1993], # 六个能力
               key_language='  航天知识感谢您的长久以来的贡献，您思考起来像二部的爱因斯坦，2019年期待您多多登录和反馈云雀哟！',  # 评价
               value_data=[0.12, 0.12, 0.12, 0.12],                              # 贡献值0.0000
               friend_name='李爱国',                                       # 好友姓名√
               friend_date='1993-12-09',                                   # 初次相遇√
               friend_time='6666',                                         # 研讨次数√
               friend_file='6',                                            # 文件交换√
               friend_content='云雀 云雀 云雀 年度 11室',                  # 讨论内容（好友）√
               team_date='1993-12-09',                                     # 创建时间√ 现在是int，最好(str)'2018-11-11'
               team_file='6',                                              # 上传文件√ int->str
               team_name='李爱国',                                         # 最佳发言人√
               team_time='8888',                                           # 团队人数√ int->str
               team_content='年报 年报 年报 年度 11室',                    # 讨论内容（团队）√(str)"121253" "发生的"
               knowledge_share='66',                                       # 贡献知识√
               knowledge_load='66',                                        # 获取知识√
               knowledge_focus='气动力与水动力设计',                       # 关注的专业√
               knowledge_best='导弹外形总体设计',                          # 擅长的专业√
               text_meeting_date='1993-12-09',                             # 初次相见
               text_talking='66',                                          # 研讨条数
               text_searching='66',                                        # 搜索条数
               text_project='66',                                          # 创建项目
               text_work='66'                                              # 创建任务
               ):  # 显示上：缺头像、雷达图、关键词、评价、科室贡献

    '''--- 第一页 ---'''
    # 处理雷达图
    radar_image = create_radar_img(name_id, user_data)  # userdata = [[数据,最大,最小值], [数据,最大,最小值], [数据,最大,最小值], [数据,最大,最小值]]
    stopwords = {"我", '你',' ', '，', '的'}
    mask = np.array(Image.open('./image/yunque.tif'))  # 遮罩
    hotwords_image = pain_word_cloud(friend_content, stopword_set=stopwords, mask=mask, userid=name_id)
    # 开画布
    can = Canvas(f"D:/toolsupload/Report/{name_id}.pdf")  # digist # D:/toolsupload/Report/user_id.pdf
    # 注册字体
    pdfmetrics.registerFont(TTFont('msyh', './ttf/msyh.ttf'))
    pdfmetrics.registerFont(TTFont('song', './ttf/汉仪大宋简.ttf'))
    can.drawImage('./image/a.png', 0, 0, 596, 843)
    # 加头像
    can.drawImage(head_image, 69, 486, height=0.53 * inch, width=0.63 * inch)
    # 加关键词
    key_words = key_words
    can.setFillColor(HexColor(0x01f7fd))
    can.setFont('song', 40)
    can.drawString(set_middle(2.3, key_words) * inch, 6.85 * inch, key_words)
    # 加雷达图
    can.drawImage(radar_image, 360, 400, 170, 170, mask='auto')
    # 关键词语解释
    can.setFillColor(HexColor(0xffffff))
    can.setFont('song', 14)
    can.drawString(0.9 * inch, 6.3 * inch, key_language[0:21])
    can.drawString(0.9 * inch, 6.0 * inch, key_language[21:43])
    can.drawString(0.9 * inch, 5.7 * inch, key_language[43:])
    '''---------------------- 我的贡献值 ----------------------'''
    can.setFillColor(HexColor(0x01f7fd))
    can.setFont('song', 18)
    can.drawString(set_middle(1.9, '{:.2%}'.format(value_data[0])) * inch, 3.55 * inch, '{:.2%}'.format(value_data[0]))
    can.drawString(set_middle(3.6, '{:.2%}'.format(value_data[1])) * inch, 3.55 * inch, '{:.2%}'.format(value_data[1]))
    can.drawString(set_middle(5.2, '{:.2%}'.format(value_data[2])) * inch, 3.55 * inch, '{:.2%}'.format(value_data[2]))
    can.drawString(set_middle(6.8, '{:.2%}'.format(value_data[3])) * inch, 3.55 * inch, '{:.2%}'.format(value_data[3]))
    '''---------------------- 年度星好友 ----------------------'''
    can.setFillColor(HexColor(0x01f7fd))
    can.setFont('song', 22)
    can.drawString(set_middle(2, friend_name) * inch, 1.9 * inch, friend_name)
    can.setFillColor(HexColor(0x01f7fd))
    can.setFont('song', 16)
    can.drawString(set_middle(1.9, friend_date) * inch, 1.2 * inch, friend_date)
    can.drawString(set_middle(2.9, friend_time) * inch, 1.2 * inch, friend_time)
    can.drawString(set_middle(2.25, friend_file) * inch, 0.4 * inch, friend_file)
    # 词云图
    can.drawImage(hotwords_image, 4.5 * inch, 0.01 * inch, 250, 170, mask='auto')
    can.showPage()                                       # showPage将保留之前的操作内容之后新建一张空白页

    '''--- 第二页 ---'''
    can.drawImage('./image/b.png', 0, 0, 596, 843)
    '''---------------------- 工作最佳团队 ----------------------'''
    mask2 = np.array(Image.open('./image/yunque2.tif'))
    hotwords_image2 = pain_word_cloud(team_content, stopword_set=stopwords, mask=mask2, userid=name_id+'s')
    can.drawImage(hotwords_image2, 4.8 * inch, 9 * inch, 250, 170, mask='auto')
    # 团队信息
    can.setFillColor(HexColor(0x01f7fd))
    can.setFont('song', 22)
    can.drawString(set_middle(2, team_name) * inch, 10.75 * inch, team_name)
    can.setFont('song', 16)
    can.drawString(set_middle(1.9, team_date) * inch, 10.15 * inch, team_date)
    can.drawString(set_middle(2.8, team_time) * inch, 10.15 * inch, team_time)
    can.drawString(set_middle(2.25, team_file) * inch, 9.35 * inch, team_file)
    '''---------------------- 知识贡献 ----------------------'''
    can.setFont('song', 20)
    can.drawString(set_middle(3, knowledge_share) * inch, 7.65*inch, knowledge_share)
    can.drawString(set_middle(6.6, knowledge_load) * inch, 7.37 * inch, knowledge_load)
    can.setFont('song', 15)
    can.drawString(5.96*inch, 7.91*inch, knowledge_focus)
    can.drawString(4.42*inch, 6.08*inch, knowledge_best)
    '''---------------------- 我的2018 ----------------------'''
    can.setFont('song', 16)
    can.drawString(set_middle(4.5, text_meeting_date) * inch, 4.85*inch, text_meeting_date)
    can.drawString(set_middle(4.65, text_talking) * inch, 4.19*inch, text_talking)
    can.drawString(set_middle(4.3, text_searching)*inch, 3.51*inch, text_searching)
    can.drawString(set_middle(3.71, text_project) * inch, 2.85 * inch, text_project)
    can.drawString(set_middle(5.02, text_work) * inch, 2.85 * inch, text_work)

    can.showPage()
    # 将所有的页内容存到打开的pdf文件里面
    can.save()
    os.remove(radar_image)
    os.remove(hotwords_image)
    os.remove(hotwords_image2)
    return f"{name_id}.pdf"
'''--- 居中 ---'''
def set_middle(x, text):
    return x-len(text)/10
'''--- 雷达图 ---'''
def create_radar_img(userid, data):
    labels = np.array(['任务', '研讨', '工具', '数据', '知识', '搜索'])
    # try:
    #     data = [(i[0]-i[2])/(i[1]-i[2]) for i in data]  # 归一化
    # except:
    #     print('数据错误')
    data = [0.01,
            0.01,
            0.01,
            0.01,
            0.01,
            0.01]
    data_max = max(data)
    data_min = min(data)
    tmpdata = []
    if (data_max == data_min) or data_max == 0:  # 三个能力相同，或者都是0
        tmpdata = [0.08,0.08,0.08,0.08,0.08,0.08]
    elif data_max*100 >= 1:
        for i in range(len(data)):
            if data[i]*10 < 0.5:
                tmpdata.append(0.5)
            else:
                tmpdata.append(data[i]*10)
    elif data_max*1000 >= 1:
        for i in range(len(data)):
            if data[i]*100 < 0.5:
                tmpdata.append(0.5)
            else:
                tmpdata.append(data[i]*100)
    elif data_max*10000 >= 1:
        for i in range(len(data)):
            tmpdata.append(data[i]*1000)

    data = tmpdata
    data.append(data[0])
    angles = [np.pi * 3 / 6, np.pi * 5 / 6, np.pi * 7 / 6, np.pi * 9 / 6, np.pi * 11 / 6, np.pi / 6]
    angles = np.concatenate((angles, [angles[0]]))
    # 处理数据
    num = 15
    mdata = []
    for i in range(num):
        tmp = [j/num*(num-i) for j in data]
        mdata.append(tmp)

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)  # polar参数！！
    for i in range(num):
        ax.plot(angles, mdata[i], 'b-', linewidth=1, alpha=0.5)
        ax.fill(angles, mdata[i], alpha=0.3, facecolor='m')  # 填充
    ax.set_thetagrids(angles * 180 / np.pi, labels, fontproperties='SimHei', fontsize=25, color='#01f7fd')
    # ax.set_title(f"{name}的雷达图", va='bottom', fontproperties="SimHei")
    ax.grid(False)  # 不显示默认的分割线
    ax.spines['polar'].set_visible(False)  # 不显示极坐标最外圈的圆
    ax.set_yticks([])  # 不显示坐标间隔
    # # 画若干个六边形
    floor = int(min(data))
    ceil = max(data)+0.01
    ax.plot(angles, [ceil] * 7, '-', lw=3, color='#01f7fd')
    # md = hashlib.md5()
    # md.update(name.encode('utf-8'))
    # digest = md.hexdigest()
    pathRadar = f'./image/radar{userid}.png'
    plt.savefig(pathRadar, format='png', bbox_inches='tight', transparent=True)
    # plt.show()
    return pathRadar  # userid,
'''--- 判断数字：中文数字、阿拉伯数字、正负小数'''
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
'''--- 分词 ---'''
def trans_CN(text, stopwords):
    word_list = jieba.cut(text)  # 不是list，是生成器，你要的时候才去生成一点，对内存有帮助 # text是所有评论用逗号隔开
    tmp = list(word_list)
    # stop = {' ', '，', '的', ',', '阿道夫'}
    stop = stopwords
    for m_word in stop:
        while m_word in tmp[::-1]:
            tmp.remove(m_word)
    # print(tmp)

    number_zh = {'一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万'}  # set 集合
    number_zh.update({f'{i}' for i in range(10)})
    for i in tmp[::-1]:  # 倒叙遍历
        if set(i) & number_zh:  # set(i)把"四个"分成"四"和"个"
            tmp.remove(i)
    # print(tmp)
    word_fre = Counter(tmp)
    # print(word_fre)
    # print(word_fre.most_common(1))
    # print(word_fre.most_common(1)[0][0])
    result = " ".join(tmp)  # result是很长的字符串，list用空格隔开变成str word_list
    return result  # 往外传
'''--- 词云 ---'''
def pain_word_cloud(
        word_string,
        scale=3,
        stopword_set=None,
        mask=None,
        font_path="./ttf/SourceHanSerifSC-Bold.otf",# C:\Windows\Fonts\STXINGKA.TTF
        randowm_state=42,
        max_font_size=150,
        userid='111111199312091111'
):
    text = trans_CN(word_string, stopword_set)
    # 设置停用词
    stopwords = set(STOPWORDS)
    stopwords.update(stopword_set)
    image_colors = ImageColorGenerator(mask)
    # 设置词云形状
    wordcloud = WordCloud(
        background_color=(255, 255, 255, 0), scale=scale, mask=mask, stopwords=stopwords, max_font_size=max_font_size,
        random_state=randowm_state, font_path=font_path, mode="RGBA"
    ).generate(text)  # mask：遮罩；random_state词云参数；font_path字体路径

    # 只用mask遮罩
    image_co = wordcloud.recolor(color_func=image_colors)
    image_produce = image_co.to_image()
    # image_produce.show()
    pathHotWords = f'./image/hotwords{userid}.png'
    image_produce.save(pathHotWords)
    return pathHotWords


if __name__ == '__main__':

    content_words = '阿道夫 123132 41 明德慎罚 哈哈 克劳德萨弗兰克 234 9001 四个 四个 四个 四个 四个人 阿道夫 你家里宽带覆盖到了分公司 你家里宽带覆盖到了分公司 41 明德慎罚 克劳德萨弗兰克 哈哈哈 这就是 我跟你说' \
                    '这艘不是 这都不是谁 硬核 太给力了 开会 明天要集体讨论 嗯 设计模式 哈哈 就这样吧 统一 同意 领导找你 对 就是这个 我不是跟你熟 来一下室办 是这个 你有' \
                    '照片么 文档发我一下 啊哪儿跟啊 在哪里开会 我在研发楼等你 打印一下报告 明天交报告 嗯嗯 好的 恩恩恩恩呢 嗯嗯 好的好的' \
                    '让我来 这是我来做 云雀 云雀 云雀 云雀 用云雀传 不用云雀传 云雀还可以 你把资料传云雀上 呼叫领导上云雀 我觉得可以 收到' \
                    '吃饭 楼下 这就来 感觉可以 真棒 先这样试试 辛苦了 发邮件 发nas 上传 光盘 刻录机 刚觉是 那本控制院里 知值奥 直到控制 ' \
                    '导航制导 仿真技术 北京故将 北京仿真中心 什么专业 不易 毕业了么 书记 主任 副主任 组长 研究院 副科长 胜利 好的 就这么牛皮'
    stopwords = {"我", '你',' ', '，', '的', ',', '了', '这', '跟', '不是', '吗','么','嘛','嗯','好的','好'}
    mask = np.array(Image.open('../image/quan.tif'))  # 遮罩
    pain_word_cloud(content_words, stopword_set=stopwords, mask=mask)  # font_path="C:\Windows\Fonts\hanyi.TTF"
    # create_pdf(friend_content=content_words)
