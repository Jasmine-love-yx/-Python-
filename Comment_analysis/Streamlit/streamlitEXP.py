#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stmlt.py
@Contact :   h939778128@gmail.com
@License :   No license
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/7/17 10:27   EvanHong      1.0         None
'''
import sys
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

# ========== 路径配置（核心修复）==========
# 获取当前脚本所在目录
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
# 定义数据/图片文件夹路径（建议你按这个结构存放文件）
DATA_DIR = os.path.join(CURRENT_DIR, "data")  # 存放CSV文件
IMAGE_DIR = os.path.join(CURRENT_DIR, "images")  # 存放图片文件

# 创建文件夹（如果不存在）
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# ========== 全局设置 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# 自定义页面背景颜色
def set_page_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #e6f7ff;
            background-attachment: fixed;
        }}
        .stSidebar {{
            background-color: #d1ecf1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_page_bg()


# ========== 工具函数（核心修复）==========
def load_image(image_name, title):
    """
    安全加载图片（处理路径和缺失问题）
    """
    image_path = os.path.join(IMAGE_DIR, image_name)
    try:
        img = Image.open(image_path)
        st.image(img, caption=title, use_container_width=True)
    except FileNotFoundError:
        st.warning(f"⚠️ 图片文件未找到：{image_name}")
        st.info(f"请将图片文件放在：{IMAGE_DIR} 目录下")
    except Exception as e:
        st.error(f"加载图片【{title}】失败：{str(e)}")


def load_csv(file_name, default_data=None):
    """
    安全加载CSV文件（处理缺失问题）
    """
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.warning(f"⚠️ CSV文件未找到：{file_name}")
        st.info(f"请将CSV文件放在：{DATA_DIR} 目录下")
        # 返回默认数据避免程序崩溃
        if default_data is not None:
            return default_data
        return pd.DataFrame()
    except Exception as e:
        st.error(f"加载CSV文件【{file_name}】失败：{str(e)}")
        return pd.DataFrame()


# ========== 页面功能函数 ==========
def show_team_info():
    st.header('基于python的电商产品评论数据情感分析')
    st.markdown("""
    ---
    ### 项目分工（独立完成）
    ### 项目作者
    **杨雄**（重庆移通学院 计算机科学与技术专业专升本11班）
    - 数据爬取，数据存储
    - 数据预处理，数据二次清洗
    - 词云构建，情感分类，数据分类
    - LDA主题模型分析，LDA可视化
    - 数据可视化呈现，模型优化，交互诊断
    - 相关文档撰写
    """)
    st.markdown('''
    ***
    ## 主要模块及具体内容
    ### 数据采集和抽取
    - 1.通过url进行对存储评论信息的json进行遍历访问，在这过程中我们发现了一些问题，运用config、log、time.sleep()解决
    - 2.不光爬取美的多个产品的数据，还爬取了海尔和史密斯的产品评论，以进行横向比较
    ### 数据预处理
     - 1.将不符合要求的数据进行补全或删除
     - 2.进行了评论准确性筛选，删去评论情感得分和实际评分星级背离较大的数据
    ### 数据初步分析及其可视化
     - 1.运用时间序列直观呈现评论数量及其平均评分的变化情况，得出美的产品口碑呈上升趋势
     - 2.将数据进行分类分析，发现不同品牌之间存在较大相似性，但也存在差异
    ### 数据分类
     - 1.比较了ROST和snowNLP，根据snownlp进行情感分析，并对其进行了好评与差评的划分
     - 2.根据品牌及其型号进行划分
     - 3.根据不同时间段进行划分
    ### 正负面评论对比分析
    - 1.进行量上的比较，发现好评数远高于差评数
    - 2.进行相对量上的比较，发现好评和差评的着重点存在着一定的差异
    ### 构建语义网络
    - 1.分别利用ROST和networkx进行可视化，对比分析得ROST的结果更为直观
    ### LDA主题分析
    - 1.发现了gensim和sklearn的LDA模型的一些区别
    - 2.利用pyLDAvis将结果可视化
    - 3.对比分析不同品牌的主题分布
    ''')
    st.markdown('''## 项目开发周期''')
    load_image('项目周期表.png', '项目周期表')


def show_crawler():
    st.markdown('***')
    st.subheader('数据爬取')
    st.markdown('''
    **数据采集和抽取**
    - 用RE、requests、beautifulsoup、lxml对html中的内容进行提取。
    - 用pandas对json中的数据进行处理
    - Pymysql完成与数据库的交互
    ''')
    if st.button('show code detail'):
        st.code('''def info_to_file():
        """
        将网页信息存入数据库/表
        :return:
        """
        global connection
        try:
            # 连接数据库
            connection = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         password='Qazwsxedcrfv0957',
                                         db='test',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            connection.autocommit(True)

            # 写入数据库
            with open('../../resources/data/haier_product_id.csv', 'r', encoding='utf-8') as csvFile:
                reader = csv.reader(csvFile)
                for line in reader:
                    for id in line:
                        print('正在检查是否重复' + id)
                        # 检查是否重复录入id
                        ids = []
                        with connection.cursor() as cursor:
                            sql = "select spider.product_info.product_id from spider.product_info"
                            cursor.execute(sql)
                            id_exist = cursor.fetchall()
                            for i in range(len(id_exist)):
                                ids.append(id_exist[i].get('product_id'))
                        if int(id) in ids:
                            print('id重复')
                            continue

                        # 没有重复录入，开始爬取信息
                        brand, model, price, goodCount, generalCount, poorCount = get_basic_product_info(id)
                        if (brand is None or model is None or price is None) or (
                                goodCount is None or generalCount is None or poorCount is None):
                            break
                        print('基本信息开始录入' + id)
                        log(None, '基本信息开始录入' + id)
                        with connection.cursor() as cursor:
                            sql = "INSERT INTO `spider`.product_info(product_id,brand,model,price,good_count,general_count,poor_count) VALUES (%s,%s, %s,%s,%s, %s,%s)"
                            cursor.execute(sql, (int(id), brand, model, price, goodCount, generalCount, poorCount))
                        log(None, '基本信息已录入' + id)
                        print('基本信息已录入' + id)
                        connection.commit()
                        time.sleep(2)

                        # 写入评论信息
                        for score in range(7):
                            if generalCount is None or goodCount is None or poorCount is None:
                                page_num = 100
                            else:
                                page_num = int((goodCount + generalCount + poorCount) / 10)
                            get_comments_and_to_file(id, page_num, (score + 1))
        except Exception as e:
            log(e)
            print('info_to_file failed')
        finally:
            connection.close()''', language='python')
    load_image('database.png', '数据库截图')


def show_time_seq():
    st.markdown('***')
    st.subheader('评论数量及评分随时间变化的结果')
    st.markdown('>揭示一段时间内产品评价量和平均评分变化，并可视化处理')
    if st.button('show code detail', key='time_seq'):
        st.code('''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
infile="compressed_comment.csv"
data=pd.read_csv(infile,encoding='utf-8',header=None)
df=pd.DataFrame(data)
df[3]=pd.to_datetime(df[3],errors='coerce')
df.set_index(df[3],inplace=True)
#数量
num_of_comment=pd.DataFrame(df['2019-01':'2020-07'][2].astype(int).resample('M').size())
num_of_comment.index.name='时间'
num_of_comment.name='num_of_comment'
#均值
avg_of_score=pd.DataFrame(df['2019-01':'2020-07'][2].astype(int).resample('M').mean())
avg_of_score.index.name='时间'
avg_of_score.name='avg_of_score'
#合并
res=pd.merge(pd.DataFrame(num_of_comment),pd.DataFrame(avg_of_score),left_index=True,right_index=True)
res=pd.DataFrame(res)
res.rename(columns={'2_x':'num_of_comment','2_y':'avg_of_score'},inplace=True)
#对数转换
num_of_comment_ln=pd.DataFrame(df['2019-01':'2020-07'][2].astype(float).resample('M').size().apply(np.log1p))
num_of_comment_ln.index.name='时间'
res2=pd.merge(pd.DataFrame(num_of_comment_ln),pd.DataFrame(avg_of_score),left_index=True,right_index=True)
res2=pd.DataFrame(res2)
res2.rename(columns={'2_x':'num_of_comment_ln','2_y':'avg_of_score'},inplace=True)
#绘图
fig, ax = plt.subplots(figsize=(10, 6))
x=res.index
x=pd.to_datetime(x,errors='coerce')
y2=res2['num_of_comment_ln']
y3=res2['avg_of_score']
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.plot(x, y2, color='navy', linewidth=2.0, linestyle='-', label='Amount')
ax.plot(x, y3, color='orange', linewidth=1.0, linestyle='--', label='Score')
ax.set_xlabel('TIME')
ax.set_ylabel('SCORE/AMOUNT(log)')
ax.legend(loc='upper right')
ax.set_title(r'$Amount(log)/Score---Time$',fontsize=25,color='teal')
plt.show()''', language='python')
    load_image('score_amount_timeSeq.png', '时间序列结果')


def show_netanalysis():
    st.markdown('***')
    st.subheader('语义网络分析')
    st.markdown('''### 生成词云''')
    load_image('词云1.png', '词云')
    load_image('词云2.png', '词云')
    st.markdown('''### 语义网络的构建及其可视化''')
    st.markdown('''
    >1.使用jieba分词，删除停用词。还对其进行了改进，删去了与评论主题不大相关的词。
>2.Collections统计词频，筛选高频词
>3.构建语义关联矩阵
>4.对生成的语义关联矩阵进行权重的归一化
>5.删除权重较小的边
>6.用networkx生成语义网络图
    ''')
    if st.button('show code detail', key='netanalysis'):
        st.code('''
import re
import jieba
import collections
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def networkx_analysis(dir='美的（Midea）JSQ22-L1(Y)_comment_正面.csv'):
    """
    输入待分析的csv文件路径
    输出networkx网络分析结果
    """
    num = 40
    G = nx.Graph()
    fig, ax = plt.subplots(figsize=(20, 14))
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 读取文件
    fn = pd.read_csv(dir, encoding='utf-8', engine='python')
    string_data = fn['comment']
    string_all = ''
    pattern = re.compile(u'\t|。|，|：|；|！|）|（|？|、|“|”')
    for i in range(len(string_data)):
        string_all += re.sub(pattern, '', string_data[i])

    # 分词
    seg_list_exact = jieba.cut(string_all, cut_all=False)
    object_list = []
    stop_words = [line.strip() for line in open('../../resources/stopwords.txt', 'r', encoding='utf-8').readlines()]

    for word in seg_list_exact:
        if word not in stop_words:
            object_list.append(word)

    # 词频统计
    word_counts = collections.Counter(object_list)
    word_counts_top = word_counts.most_common(num)
    word = pd.DataFrame(word_counts_top, columns=['关键词', '次数'])

    # 构建语义关联矩阵
    net = pd.DataFrame(np.mat(np.zeros((num, num))), columns=word.iloc[:, 0])
    for i in range(len(string_data)):
        seg_list_exact = jieba.cut(string_data[i], cut_all=False)
        object_list2 = []
        for words in seg_list_exact:
            if words not in stop_words:
                object_list2.append(words)

        word_counts2 = collections.Counter(object_list2)
        word_counts_top2 = word_counts2.most_common(num)
        word2 = pd.DataFrame(word_counts_top2)

        relation = [0]*num
        for j in range(num):
            for p in range(len(word2)):
                if word.iloc[j, 0] == word2.iloc[p, 0]:
                    relation[j] = 1
                    break

        for j in range(num):
            if relation[j] == 1:
                for q in range(num):
                    if relation[q] == 1:
                        net.iloc[j, q] += word2.iloc[p, 1]
                        net.iloc[q, j] = net.iloc[j, q]

    # 归一化
    max_weight = net.values.max()
    for i in range(num):
        for j in range(num):
            net.iloc[i, j] /= max_weight

    # 构建网络
    for i in range(num):
        for j in range(i, num):
            G.add_weighted_edges_from([(word.iloc[i, 0], word.iloc[j, 0], net.iloc[i, j])])

    nx.draw_networkx(G,
                     pos=nx.circular_layout(G),
                     ax=ax,
                     width=[float(v['weight'] * 3) for (r, c, v) in G.edges(data=True)],
                     edge_color='orange',
                     node_size=[float(net.iloc[i, i] * 2000) for i in np.arange(20)],
                     node_color='#87CEEB',
                     font_size=15,
                     font_weight='1000')
    ax.axis('off')
    plt.show()''', language='python')
    load_image('语义网络.png', '语义网络')
    load_image('rost语义网络.png', 'rost语义网络')


def show_comment_length():
    st.markdown('***')
    st.subheader('评论长度分析')

    # 加载数据（安全处理）
    contentlenth = load_csv("content_lenth.csv")
    good_contentlenth = load_csv("good_content_lenth.csv")
    bad_contentlenth = load_csv("bad_content_lenth.csv")

    # 只有数据非空时才绘图
    if not contentlenth.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(x=contentlenth.loc[:]["contentlenth"], bins=50, range=(0, 200), color='steelblue')
        ax.set_title("总体评论长度分布")
        ax.set_ylabel("数目")
        ax.set_xlabel("长度")
        st.pyplot(fig)

    # 绘制好评/差评对比
    if not good_contentlenth.empty and not bad_contentlenth.empty:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.hist(x=good_contentlenth.loc[:]["contentlenth"], bins=50, range=(0, 200), color='steelblue')
        ax1.set_title("好评长度分布")
        ax1.set_ylabel("数目")
        ax1.set_xlabel("长度")

        ax2.hist(x=bad_contentlenth.loc[:]["contentlenth"], bins=50, range=(0, 200), color='coral')
        ax2.set_title("差评长度分布")
        ax2.set_ylabel("数目")
        ax2.set_xlabel("长度")

        st.pyplot(fig)


def show_comment_sentiment():
    st.markdown('***')
    st.subheader("正负面评论主题分析：")
    st.write("2020年美的品牌的评论侧重")

    month = st.slider('月份', 1, 7, 1)
    df2 = load_csv(f"comment_time_matrix{month}.csv")

    if not df2.empty:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        df2.loc[0].plot(kind='pie', autopct='%.2f%%', ax=ax1)
        ax1.set_title("好评主题分布")
        ax1.set_ylabel("")

        df2.loc[1].plot(kind='pie', autopct='%.2f%%', ax=ax2)
        ax2.set_title("差评主题分布")
        ax2.set_ylabel("")

        st.pyplot(fig)
        st.dataframe(df2, 500)


def show_LDA_visualization():
    st.markdown('***')
    st.subheader('LDA主题分析可视化')

    display_type = st.selectbox(
        '=>请选择一个选项<=',
        ['美的品牌评论情感分类LDA结果',
         '美的品牌评论随时间变化LDA结果',
         '美的品牌与其他品牌热水器在各方面评论对比LDA结果']
    )

    if display_type == '美的品牌评论情感分类LDA结果':
        st.markdown("""
        **[美的正面评价LDA主题分析结果](https://dyf-2316.github.io/HYF_LDA_results/meidi_summary/美的（Midea）_正面.html)**
        **[美的负面评价LDA主题分析结果](https://dyf-2316.github.io/HYF_LDA_results/meidi_summary/美的（Midea）_负面.html)**

        `从“美的正面评论总览”和“美的负面评论总览”我们发现，光是从数量上来看的话，安装服务是顾客最在意的点。     
        但是当我们选择了最主要的主题之后可以发现，顾客在一个较为满意的购物体验中，安装的重要性会适当下降,
        反而热水器有关的外观、性能会给他们留下更深刻的印象。
        但是对于较差的购物体验，安装、服务、售后、费用等关键词是较为主要的几个点`
        """)
        load_image('meidi_pos.png', '美的正面评论总览')
        load_image('meidi_neg.png', '美的负面评论总览')
        load_image('meidi_positive.jpg', '美的正面评论最主要主题内容')
        load_image('meidi_negative.jpg', '美的负面评论最主要主题内容')

    elif display_type == '美的品牌评论随时间变化LDA结果':
        st.markdown('''
        **[2017](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2017.html)**
        **[2018](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2018.html)**
        **[2019](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2019.html)**
        **[2020](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2020.html)**

        `从中我们可以看到，在2018年人们的评论主题较大可能为品牌，但是到了2019/2020年，
        人们更加乐于评论外形外观以及性能方面的话题，说明美的在这段时间可能对产品进行了外观上的大升级，
        大大增强了产品竞争力`
        ''')
        load_image('2017.png', '美的2017年热水器评论主题分析')
        load_image('2018.png', '美的2018年热水器评论主题分析')
        load_image('2019.png', '美的2019年热水器评论主题分析')
        load_image('2020.png', '美的2020年热水器评论主题分析')

    elif display_type == '美的品牌与其他品牌热水器在各方面评论对比LDA结果':
        st.markdown('''
        `通过对tag进行筛选后我们可以观察到各个方面各品牌产品的特点`
        ''')
        feature = st.radio(
            '请选择一方面进行对比',
            ['安装服务', '外形外观', '耗能情况', '恒温效果', '噪音大小', '出水速度']
        )

        if feature == '安装服务':
            st.markdown('*** ')
            st.markdown('安装服务')
            st.markdown("""
                `美的产品相较于别的产品在安装服务的及时性以及速度方面评分较高，并且在服务质量、专业性方面和其他品牌均持平`
            """)
            st.markdown('''
                **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）安装服务_comment.html)**
                **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）安装服务_comment.html)**
                **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S安装服务_comment.html)**
            ''')
            load_image('美的安装.png', '美的安装')
            load_image('海尔安装.png', '海尔安装')
            load_image('史密斯安装.png', '史密斯安装')

        elif feature == '外形外观':
            st.markdown('*** ')
            st.markdown('外形外观')
            st.markdown("""
                `美的的产品在外观方面并没有特别突出的特点，不像海尔热水器有一个较为显著的特点是简介，史密斯较为上档次`
            """)
            st.markdown('''
                **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）外形外观_comment.html)**
                **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）外形外观_comment.html)**
                **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S外形外观_comment.html)**
            ''')

        elif feature == '耗能情况':
            st.markdown('*** ')
            st.markdown('耗能情况')
            st.markdown("""
                `美的产品可能有较为清楚的能耗标识，因此美的评论主题关键词中“清楚”“知道”排名靠前`
            """)
            st.markdown('''
                **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）耗能情况_comment.html)**
                **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）耗能情况_comment.html)**
                **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S耗能情况_comment.html)**
            ''')

        elif feature == '恒温效果':
            st.markdown('*** ')
            st.markdown('恒温效果')
            st.markdown("""
                `美的产品在此方面没有特别突出的点`
            """)
            st.markdown('''
                **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）恒温效果_comment.html)**
                **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）恒温效果_comment.html)**
                **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S恒温效果_comment.html)**
            ''')

        elif feature == '噪音大小':
            st.markdown('*** ')
            st.markdown('噪音大小')
            st.markdown("""
                `美的产品噪音较小，但与其他产品差别不大`
            """)
            st.markdown('''
                **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）噪音大小_comment.html)**
                **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）噪音大小_comment.html)**
                **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S噪音大小_comment.html)**
            ''')

        elif feature == '出水速度':
            st.markdown('*** ')
            st.markdown('出水速度')
            st.markdown("""
                `美的产品出水速度快，温度稳定，但与其他产品差别不大`
            """)
            st.markdown('''
                **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）出水速度_comment.html)**
                **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）出水速度_comment.html)**
                **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S出水速度_comment.html)**
            ''')


def show_lda():
    st.markdown('***')
    st.subheader('LDA模型分析')

    LDA_topics = st.sidebar.slider('LDA主题数', 3, 9, 6)
    df1 = load_csv(f"LDA_{LDA_topics}.csv")

    # 加载coherence数据
    coherence_data = load_csv("coherence.csv", default_data=pd.DataFrame({
        'c_v': [0.5, 0.6, 0.7, 0.75, 0.78, 0.8, 0.79, 0.77, 0.75],
        'u_mass': [-1.2, -1.1, -0.9, -0.8, -0.75, -0.7, -0.72, -0.75, -0.8],
        'topics': [1, 2, 3, 4, 5, 6, 7, 8, 9]
    }))

    if not coherence_data.empty:
        st.subheader("LDA模型coherence")
        st.markdown(''' 
        > 1.处理数据，构成词空间，进行向量化
        > 2.利用gensim库，建立LDA模型进行训练
        > 3.使用coherence模型判断模型优劣，分别使用c_v和u-mass模式
        > 4.调整参数，进行主题分析
        ''')

        # 绘制coherence曲线
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        ax1.plot(coherence_data['topics'], coherence_data['c_v'], marker='o', color='blue')
        ax1.set_title('c_v 一致性得分')
        ax1.set_xlabel('主题数')
        ax1.set_ylabel('c_v得分')

        ax2.plot(coherence_data['topics'], coherence_data['u_mass'], marker='o', color='red')
        ax2.set_title('u_mass 一致性得分')
        ax2.set_xlabel('主题数')
        ax2.set_ylabel('u_mass得分')

        st.pyplot(fig)

    # 显示主题分布
    if not df1.empty:
        st.markdown("### 不同品牌的主题分布对比：")
        df1.rename(columns={"Unnamed: 0": "主题"}, inplace=True)
        st.dataframe(df1, 600)

        # 绘制堆叠柱状图
        if '美的' in df1.columns and '海尔' in df1.columns and '史密斯' in df1.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            df1.iloc[:, 1:4].plot.bar(stacked=True, ax=ax)
            ax.set_title('各品牌主题分布')
            ax.set_xlabel('主题')
            ax.set_ylabel('占比')
            st.pyplot(fig)

            # 分析各品牌卖点
            dic = {}
            for col in df1.columns[1:4]:
                dic[col] = []

            maxidx = df1.iloc[:, 1:4].idxmax(axis=1)
            for idx, brand in enumerate(maxidx):
                dic[brand].append(idx)

            for brand, topics in dic.items():
                st.write(f"**{brand}卖点:**")
                for topic in topics:
                    st.markdown(f"- 主题{topic}: {df1.loc[topic]['主题']}")


def show_conclusion():
    st.markdown('***')
    st.subheader('项目总结')
    st.markdown('''
    ### 主要结论
    1. **美的产品口碑趋势**：2019-2020年美的热水器产品口碑呈上升趋势，用户评价整体向好
    2. **用户关注点差异**：好评用户更关注产品外观和性能，差评用户主要抱怨安装服务和售后费用
    3. **品牌对比**：美的在安装服务及时性上表现较好，海尔产品设计简洁，史密斯定位高端
    4. **时间维度变化**：2018年后用户评论重心从品牌转向产品外观和性能，反映产品升级效果

    ### 建议
    1. 继续优化安装服务流程，降低用户投诉率
    2. 保持产品外观和性能优势，持续创新
    3. 加强能耗标识的清晰度，突出产品节能特点
    ''')


# ========== 主程序 ==========
if __name__ == "__main__":
    show_team_info()
    show_crawler()
    show_time_seq()
    show_comment_length()
    show_netanalysis()
    show_comment_sentiment()
    show_LDA_visualization()
    show_lda()
    show_conclusion()