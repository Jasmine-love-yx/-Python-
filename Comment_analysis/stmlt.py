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
# ========== 第一步：修复路径和基础配置 ==========
import sys
import os
import logging

# 1. 配置log函数（解决爬取代码中log()缺失问题）
logging.basicConfig(filename='app.log', level=logging.ERROR)


def log(e):
    logging.error(str(e))


# 2. 获取当前文件（stmlt.py）的路径（关键！适配你的目录）
# stmlt.py在Comment_analysis文件夹下，所以cur_dir是Comment_analysis的路径
cur_dir = os.path.dirname(os.path.abspath(__file__))
# 项目根路径：Comment_analysis的上一级（E:\Comment-analysis-master）
root_path = os.path.dirname(cur_dir)
# 添加根路径到sys.path，方便导入configs等
sys.path.append(root_path)
sys.path.append(cur_dir)

# 3. 定义图片/数据的绝对路径（适配你的目录）
# 图片路径：根目录/resources/LDA_related/pictures
IMAGE_PATH = os.path.join(root_path, "resources", "LDA_related", "pictures")
# 数据路径：Comment_analysis/data
DATA_PATH = os.path.join(cur_dir, "data")

# 4. 修复Matplotlib后端（适配Streamlit绘图）
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ========== 第二步：导入依赖库 ==========
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import configs.config as cf  # 你的目录有configs，不用注释！

# 5. 解决中文/负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# ========== 第三步：修复自定义函数 ==========
# 修复页面背景函数（不变）
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


# 修复图片加载函数（用定义好的IMAGE_PATH）
def show_image(image_name, title):
    try:
        st.image(Image.open(image_name), caption=title, use_container_width=True)
    except FileNotFoundError:
        st.warning(f"⚠️ 缺少图片文件：{image_name}，已跳过显示【{title}】")
    except Exception as e:
        st.error(f"加载图片【{title}】失败：{str(e)}")


# ========== 第四步：修改所有涉及路径的函数 ==========
# 1. 修复show_team_info（项目周期表图片路径）
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
    ***\n   
    ## 主要模块及具体内容 \n
    ### 数据采集和抽取 \n
    - 1.通过url进行对存储评论信息的json进行遍历访问，在这过程中我们发现了一些问题，运用config、log、time.sleep()解决\n
    - 2.不光爬取美的多个产品的数据，还爬取了海尔和史密斯的产品评论，以进行横向比较 \n
    ### 数据预处理\n
     - 1.将不符合要求的数据进行补全或删除\n
     - 2.进行了评论准确性筛选，删去评论情感得分和实际评分星级背离较大的数据 \n
    ### 数据初步分析及其可视化\n
     - 1.运用时间序列直观呈现评论数量及其平均评分的变化情况，得出美的产品口碑呈上升趋势
     - 2.将数据进行分类分析，发现不同品牌之间存在较大相似性，但也存在差异 \n
    ### 数据分类\n
     - 1.比较了ROST和snowNLP，根据snownlp进行情感分析，并对其进行了好评与差评的划分
     - 2.根据品牌及其型号进行划分
     - 3.根据不同时间段进行划分
    ### 正负面评论对比分析 \n
    - 1.进行量上的比较，发现好评数远高于差评数\n
    - 2.进行相对量上的比较，发现好评和差评的着重点存在着一定的差异 \n
    ### 构建语义网络 \n
    - 1.分别利用ROST和networkx进行可视化，对比分析得ROST的结果更为直观 \n
    ### LDA主题分析 \n
    - 1.发现了gensim和sklearn的LDA模型的一些区别\n
    - 2.利用pyLDAvis将结果可视化 \n
    - 3.对比分析不同品牌的主题分布\n
    ''')
    st.markdown('''## 项目开发周期''')
    # 关键：改用定义好的图片路径
    project_cycle_img = os.path.join(IMAGE_PATH, "项目周期表.png")
    show_image(project_cycle_img, '项目周期表')


# 2. 修复show_crawler（数据库截图路径）
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
                                         cursorclass=pymysql.cursors.DictCursor
                                         )
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
                            # 创建一条新的记录
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
                        # 如果信息为空，则不录入
                        if (brand is None or model is None or price is None) or (
                                goodCount is None or generalCount is None or poorCount is None):
                            break
                        print('基本信息开始录入' + id)
                        log(None, '基本信息开始录入' + id)
                        with connection.cursor() as cursor:
                            # 创建一条新的记录
                            sql = "INSERT INTO `spider`.product_info(product_id,brand,model,price,good_count,general_count,poor_count) VALUES (%s,%s, %s,%s,%s, %s,%s)"
                            cursor.execute(sql, (int(id), brand, model, price, goodCount, generalCount, poorCount))
                        log(None, '基本信息已录入' + id)
                        print('基本信息已录入' + id)

                        # 连接完数据库并不会自动提交，所以需要手动 commit 你的改动
                        connection.commit()
                        time.sleep(2)

                        # write comment related information into table comments
                        # 不同的评论种类，其中包含带图评论等
                        for score in range(7):
                            # 如果有一个数量为空，则默认最大读取页数为100
                            if generalCount is None or goodCount is None or poorCount is None:
                                page_num = 100
                            else:  # 否则计算最大页数
                                page_num = int((goodCount + generalCount + poorCount) / 10)
                            get_comments_and_to_file(id, page_num, (score + 1))
        except Exception as e:
            log(e)
            print('info_to_file failed')

        finally:
            connection.close()
    ''')
    # 关键：数据库截图路径
    db_img = os.path.join(IMAGE_PATH, "database.png")
    show_image(db_img, '数据库截图')


# 3. 修复show_netanalysis（标题错误+图片路径）
def show_netanalysis():
    st.markdown('***')
    # 修复错误标题：从“评论数量及评分”改成“语义网络分析”
    st.subheader('语义网络分析（词云+语义网络构建）')
    st.markdown('''### 生成词云''')
    # 词云图片路径
    wordcloud1 = os.path.join(IMAGE_PATH, "词云1.png")
    wordcloud2 = os.path.join(IMAGE_PATH, "词云2.png")
    show_image(wordcloud1, '词云')
    show_image(wordcloud2, '词云')

    st.markdown('''### 语义网络的构建及其可视化\n''')
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
import re  # 正则表达式库
import jieba  # 分词
import collections  # 词频统计库
import numpy as np
import pandas as pd
import networkx as nx  # 复杂网络分析库
import matplotlib.pyplot as plt

def networkx_analysis(dir='美的（Midea）JSQ22-L1(Y)_comment_正面.csv'):
    """
    输入待分析的csv文件路径
    输出networkx网络分析结果
    """
    # 初始化
    num = 40
    G = nx.Graph()
    plt.figure(figsize=(20, 14))
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    # 读取文件
    fn = pd.read_csv(dir, encoding='utf-8', engine='python')  # 打开文件
    string_data = fn['comment']  # 读出评论文件
    print(len(string_data))
    file = open('meidi.txt', 'w')

    string_all = ''
    # 文本预处理
    pattern = re.compile(u'\t|。|，|：|；|！|）|（|？|、|“|”')  # 定义正则表达式匹配模式
    for i in range(len(string_data)):
        string_all += re.sub(pattern, '', string_data[i])
        file.write(string_data[i] + '\n')

    # 文本分词
    seg_list_exact = jieba.cut(string_all, cut_all=False)  # 精确模式分词
    object_list = []
    stop_words = []
    file = open('../../resources/stopwords.txt', 'r', encoding='utf-8').readlines()  # 自定义去除词库
    for each_line in file:
        each_line = each_line.strip('\n')
        stop_words.append(each_line)
    print(stop_words)

    for word in seg_list_exact:  # 循环读出每个分词
        if word not in stop_words:  # 如果不在去除词库中
            object_list.append(word)  # 分词追加到列表

    print('object_list的个数：', len(object_list))
    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(num)  # 获取最高频的词
    word = pd.DataFrame(word_counts_top, columns=['关键词', '次数'])
    print(word)

    net = pd.DataFrame(np.mat(np.zeros((num, num))), columns=word.iloc[:, 0])

    print('===' * 30)

    k = 0
    object_list2 = []
    # 构建语义关联矩阵
    for i in range(len(string_data)):
        seg_list_exact = jieba.cut(string_data[i], cut_all=False)  # 精确模式分词
        object_list2 = []
        for words in seg_list_exact:  # 循环读出每个分词
            if words not in stop_words:  # 如果不在去除词库中
                object_list2.append(words)  # 分词追加到列表

        word_counts2 = collections.Counter(object_list2)
        word_counts_top2 = word_counts2.most_common(num)  # 获取该段最高频的词
        word2 = pd.DataFrame(word_counts_top2)
        word2_T = pd.DataFrame(word2.values.T, columns=word2.iloc[:, 0])

        relation = list(0 for x in range(num))
        # 查看该段最高频的词是否在总的最高频的词列表中
        for j in range(num):
            for p in range(len(word2)):
                if word.iloc[j, 0] == word2.iloc[p, 0]:
                    relation[j] = 1
                    break
                # 对于同段落内出现的最高频词，根据其出现次数加到语义关联矩阵的相应位置
        for j in range(num):
            if relation[j] == 1:
                for q in range(num):
                    if relation[q] == 1:
                        net.iloc[j, q] = net.iloc[j, q] + word2_T.loc[1, word.iloc[q, 0]]
                        net.iloc[q, j] = net.iloc[j, q] + word2_T.loc[1, word.iloc[q, 0]]
    net.to_excel('net.xls')
    print(net)
    # 处理最后一段内容，完成语义关联矩阵的构建
    max_weight = net.values.max()  # 修复get_values()为values
    # 数据归一化
    for i in range(num):
        for j in range(num):
            net.iloc[i, j] = net.iloc[i, j] / max_weight
    n = len(word)
    # 边的起点，终点，权重
    for i in range(n):
        for j in range(i, n):
            G.add_weighted_edges_from([(word.iloc[i, 0], word.iloc[j, 0], net.iloc[i, j])])
    nx.draw_networkx(G,
                     pos=nx.circular_layout(G),
                     width=[float(v['weight'] * 3) for (r, c, v) in G.edges(data=True)],
                     edge_color='orange',
                     node_size=[float(net.iloc[i, i] * 2000) for i in np.arange(20)],
                     node_color='#87CEEB',
                     font_size=15,
                     font_weight='1000',
                     )

    plt.axis('off')
    plt.show(G)
        ''')
    # 语义网络图片路径
    net_img1 = os.path.join(IMAGE_PATH, "语义网络.png")
    net_img2 = os.path.join(IMAGE_PATH, "rost语义网络.png")
    show_image(net_img1, '语义网络')
    show_image(net_img2, 'rost语义网络')


# 4. 修复show_lda（csv路径+get_values()错误）
def show_lda():
    st.markdown('***')
    LDA_topics = st.sidebar.slider('LDA主题数', 3, 9, 6)
    # 新增异常捕获+正确的csv路径
    try:
        df1 = pd.read_csv(os.path.join(DATA_PATH, f"LDA_{LDA_topics}.csv"))
    except FileNotFoundError:
        st.error(f"找不到文件：LDA_{LDA_topics}.csv，请检查Comment_analysis/data文件夹下是否有该文件")
        return

    # 读取coherence.txt（放在data文件夹）
    try:
        with open(os.path.join(DATA_PATH, 'coherence.txt'), 'r') as f:
            s1 = f.readline()
            s2 = f.readline()
    except FileNotFoundError:
        st.error("找不到coherence.txt，请检查Comment_analysis/data文件夹下是否有该文件")
        return

    s1 = [float(i) for i in s1.split(" ") if i.strip()]
    s2 = [float(i) for i in s2.split(" ") if i.strip()]
    s = np.array([s1, s2])
    coherence = pd.DataFrame(s, index=['c_v', 'u_mass'], columns=np.arange(1, len(s1) + 1))
    st.subheader("LDA模型coherence")
    st.markdown(''' 
    > 1.处理数据，构成词空间，进行向量化
    > 2.利用gensim库，建立LDA模型进行训练
    > 3.使用coherence模型判断模型优劣，分别使用c_v和u-mass模式
    > 4.调整参数，进行主题分析
    ''')
    st.dataframe(coherence, 1200)

    s1_df = pd.DataFrame(s1, index=np.arange(1, len(s1) + 1), columns=["c_v"])
    st.line_chart(s1_df)
    s2_df = pd.DataFrame(s2, index=np.arange(1, len(s2) + 1), columns=["u_mass"])
    st.line_chart(s2_df)

    st.markdown("### 不同品牌的主题分布对比：")
    st.markdown('''
       > 1.使用genism中的lda模型进行主题分析
> 2.对每条评论进行归属主题判断，得出不同品牌商品的评论侧重
> 3.使用matplotlib绘图进行展示
    ''')

    df1.rename(columns={"Unnamed: 0": "主题"}, inplace=True)
    st.dataframe(df1, 600)

    df1.iloc[:, 1:4].plot.bar(stacked=True)
    st.pyplot()

    df_2 = pd.DataFrame(df1.iloc[:, 1:4].values, index=df1.iloc[:, 1:4].index, columns=df1.iloc[:, 1:4].columns)
    st.dataframe(df_2, 1000)

    df_2.plot.hist(alpha=0.5)
    st.pyplot()
    dic = {}
    for i in df1.columns:
        dic[i] = []
    maxidx = df1.iloc[:, 1:4].idxmax(axis=1)

    for idx, i in enumerate(maxidx):
        dic[i].append(idx)

    for brand, topics in dic.items():
        st.write(brand + "卖点:")
        for topic in topics:
            st.markdown("- 主题" + str(topic) + ":" + df1.loc[topic]['主题'])


# 5. 修复show_comment_sentiment（csv路径）
def show_comment_sentiment():
    st.markdown('***')
    st.subheader("正负面评论主题分析：")
    st.write("2020年美的品牌的评论侧重")
    month = st.slider('月份', 1, 7, 1)
    # 异常捕获+正确路径
    try:
        df2 = pd.read_csv(os.path.join(DATA_PATH, f"comment_time_matrix{month}.csv"))
    except FileNotFoundError:
        st.error(f"找不到文件：comment_time_matrix{month}.csv，请检查Comment_analysis/data文件夹下是否有该文件")
        return

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.5, hspace=None)

    df2.loc[0].plot(kind='pie', autopct='%.2f%%')
    plt.title("好评")
    st.pyplot()

    df2.loc[1].plot(kind='pie', autopct='%.2f%%')
    plt.title("差评")
    st.pyplot()
    st.dataframe(df2, 500)


# 6. 修复show_comment_length（csv路径）
def show_comment_length():
    st.markdown('***')
    # 异常捕获+正确路径
    try:
        contentlenth = pd.read_csv(os.path.join(DATA_PATH, "content_lenth.csv"))
        good_contentlenth = pd.read_csv(os.path.join(DATA_PATH, "good_content_lenth.csv"))
        bad_contentlenth = pd.read_csv(os.path.join(DATA_PATH, "bad_content_lenth.csv"))
    except FileNotFoundError as e:
        st.error(f"找不到文件：{e.filename}，请检查Comment_analysis/data文件夹下是否有该文件")
        return

    plt.hist(x=contentlenth.loc[:]["contentlenth"], bins=50, range=(0, 200), color='steelblue')
    plt.title("总体评论")
    plt.ylabel("数目")
    plt.xlabel("长度")
    st.pyplot()

    plt.subplot(2, 2, 1)
    plt.hist(x=good_contentlenth.loc[:]["contentlenth"], bins=50, range=(0, 200), color='steelblue')
    plt.title("好评")
    plt.ylabel("数目")
    plt.xlabel("长度")

    plt.subplot(2, 2, 2)
    plt.hist(x=bad_contentlenth.loc[:]["contentlenth"], bins=50, range=(0, 200), color='steelblue')
    plt.title("差评")
    plt.ylabel("数目")
    plt.xlabel("长度")
    st.pyplot()


# 其他函数（show_LDA_visualization、show_time_seq等）按相同逻辑修改图片路径：
# 比如show_LDA_visualization中的meidi_pos.png → os.path.join(IMAGE_PATH, "meidi_pos.png")
def show_LDA_visualization():
    st.markdown('***')
    st.subheader('LDA主题分析可视化')
    st.markdown("""
    - 构建相应的语料库
    - 使用sklearn库进行模型训练
    - 利用pyLDAvis库将模型可视化
    """)
    st.markdown('**进入以下超链接可直接进行互动**')
    st.markdown('>更改lambda值（0-1）可以查看每个主题最具特点的词-每个主题最主要的词（类似于tf idf）')
    display_type = st.selectbox('=>请选择一个选项<=', ['美的品牌评论情感分类LDA结果', '美的品牌评论随时间变化LDA结果',
                                                       '美的品牌与其他品牌热水器在各方面评论对比LDA结果'])
    if display_type == '美的品牌评论情感分类LDA结果':
        st.markdown("""
            **[美的正面评价LDA主题分析结果](https://dyf-2316.github.io/HYF_LDA_results/meidi_summary/美的（Midea）_正面.html)**\n
            **[美的负面评价LDA主题分析结果](https://dyf-2316.github.io/HYF_LDA_results/meidi_summary/美的（Midea）_负面.html)**\n\n
        """)
        st.markdown("""
            `从“美的正面评论总览”和“美的负面评论总览”我们发现，光是从数量上来看的话，安装服务是顾客最在意的点。     
            但是当我们选择了最主要的主题之后可以发现，顾客在一个较为满意的购物体验中，安装的重要性会适当下降,
            反而热水器有关的外观、性能会给他们留下更深刻的印象。
            但是对于较差的购物体验，安装、服务、售后、费用等关键词是较为主要的几个点`
        """)
        # 修复图片路径
        meidi_pos = os.path.join(IMAGE_PATH, "meidi_pos.png")
        meidi_neg = os.path.join(IMAGE_PATH, "meidi_neg.png")
        meidi_positive = os.path.join(IMAGE_PATH, "meidi_positive.jpg")
        meidi_negative = os.path.join(IMAGE_PATH, "meidi_negative.jpg")
        show_image(meidi_pos, '美的正面评论总览')
        show_image(meidi_neg, '美的负面评论总览')
        show_image(meidi_positive, '美的正面评论最主要主题内容')
        show_image(meidi_negative, '美的负面评论最主要主题内容')
    elif display_type == '美的品牌评论随时间变化LDA结果':
        st.markdown('''
            **[2017](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2017.html)**\n
            **[2018](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2018.html)**\n
            **[2019](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2019.html)**\n
            **[2020](https://dyf-2316.github.io/HYF_LDA_results/meidi_yearly_comment/spider_meidi_comments2020.html)**\n
            `从中我们可以看到，在2018年人们的评论主题较大可能为品牌，但是到了2019/2020年，
            人们更加乐于评论外形外观以及性能方面的话题，说明美的在这段时间可能对产品进行了外观上的大升级，
            大大增强了产品竞争力`
        ''')
        # 修复图片路径
        img2017 = os.path.join(IMAGE_PATH, "2017.png")
        img2018 = os.path.join(IMAGE_PATH, "2018.png")
        img2019 = os.path.join(IMAGE_PATH, "2019.png")
        img2020 = os.path.join(IMAGE_PATH, "2020.png")
        show_image(img2017, '美的2017年热水器评论主题分析')
        show_image(img2018, '美的2018年热水器评论主题分析')
        show_image(img2019, '美的2019年热水器评论主题分析')
        show_image(img2020, '美的2020年热水器评论主题分析')
    elif display_type == '美的品牌与其他品牌热水器在各方面评论对比LDA结果':
        st.markdown('''
            `通过对tag进行筛选后我们可以观察到各个方面各品牌产品的特点`
        ''')
        feature = st.radio('请选择一方面进行对比',
                           ['安装服务', '外形外观', '耗能情况', '恒温效果', '噪音大小', '出水速度'])
        if feature == '安装服务':
            st.markdown('*** ')
            st.markdown('安装服务')
            st.markdown("""
                `美的产品相较于别的产品在安装服务的及时性以及速度方面评分较高，并且在服务质量、专业性方面和其他品牌均持平`
            """)
            st.markdown('''
                            **[美的](https://dyf-2316.github.io/HYF_LDA_results/tag/美的（Midea）安装服务_comment.html)**\n
                            **[海尔](https://dyf-2316.github.io/HYF_LDA_results/tag/海尔（Haier）安装服务_comment.html)**\n
                            **[史密斯](https://dyf-2316.github.io/HYF_LDA_results/tag/史密斯（A.O.S安装服务_comment.html)**\n
                        ''')
            # 修复图片路径
            md_install = os.path.join(IMAGE_PATH, "美的安装.png")
            he_install = os.path.join(IMAGE_PATH, "海尔安装.png")
            sm_install = os.path.join(IMAGE_PATH, "史密斯安装.png")
            show_image(md_install, '美的安装')
            show_image(he_install, '海尔安装')
            show_image(sm_install, '史密斯安装')
        # 其他feature（外形外观/耗能等）如果有图片，也按这个方式修改路径


# 保留原有show_time_seq、show_conclusion函数（无路径问题）
def show_time_seq():
    st.markdown('***')
    st.subheader('评论数量及评分随时间变化的结果')
    st.markdown('>揭示一段时间内产品评价量和平均评分变化，并可视化处理')
    if st.button('show code detail', key='time_seq'):
        st.code('''import pandas as pd
import matplotlib
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
infile="compressed_comment.csv"
data=pd.read_csv(infile,encoding='utf-8',header=None)
data.head()
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
print(res)
#ln&e
num_of_comment_ln=pd.DataFrame(df['2019-01':'2020-07'][2].astype(float).resample('M').size().apply(np.log1p))
num_of_comment_ln.index.name='时间'
res2=pd.merge(pd.DataFrame(num_of_comment_ln),pd.DataFrame(avg_of_score),left_index=True,right_index=True)
res2=pd.DataFrame(res2)
res2.rename(columns={'2_x':'num_of_comment_ln','2_y':'avg_of_score'},inplace=True)
print(res2)

#plt
x=res.index
x=pd.to_datetime(x,errors='coerce')
y1=res['num_of_comment']
y2=res2['num_of_comment_ln']
y3=res2['avg_of_score']
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
#plt.plot(x, y1, color='teal', linewidth=1.0, linestyle='-', label='predict')#原评论
plt.plot(x, y2, color='navy', linewidth=2.0, linestyle='-', label='predict')#对数后的评论量
plt.plot(x, y3, color='orange', linewidth=1.0, linestyle='--', label='predict')#平均分
plt.xlabel('TIME')
plt.ylabel('SCORE/AMOUNT(log)')
plt.legend(['Amount','Score'],loc='upper right')
plt.title(r'$Amount(log)/Score---Time$',fontsize=25,color='teal')
plt.show()
    ''')
    # 修复时间序列图片路径
    time_seq_img = os.path.join(IMAGE_PATH, "score_amount_timeSeq.png")
    show_image(time_seq_img, '时间序列结果')


def show_conclusion():
    pass


# ========== 最后：运行所有函数 ==========
show_team_info()
show_crawler()
show_time_seq()
show_comment_length()
show_netanalysis()
show_comment_sentiment()
show_LDA_visualization()
show_lda()
show_conclusion()