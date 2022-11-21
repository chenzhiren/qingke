import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
import numpy as np

# 金额分层
def fen_ceng(data):
    data['fenceng'] = 1
    for i in range(data.shape[0]):
        if type(data.iloc[i, 13]) == type(1.1):
            data.iloc[i, 14] = '有具体数据'
        if type(data.iloc[i, 13]) == type('abc'):
            data.iloc[i, 14] = '文字数据'
        if data.iloc[i, 13] ==1:
            data.iloc[i, 14] = '无数据'
        if data.iloc[i,13]==type(1):
            data.iloc[i,14]= '有具体数据'
    return data


# 去除括号方法
def one(w):
    if '[]' in w:
        w = w.replace('[]', '')
    else:
        w = w.replace("['", '').replace("']", '')
    return w


# 去除数据的括号
def clean_1(data):
    data['business'] = data['business'].apply(one)
    data['round'] = data['round'].apply(one)
    data['currency'] = data['currency'].apply(one)
    data['money'] = data['money'].apply(one)
    data['investers'] = data['investers'].apply(one)
    return data


# 区分国内外项目
def in_out(data):
    import re
    data['in_out'] = 1
    for i in range(len(data)):
        a = data.iloc[i, 1]
        b = re.findall('[a-zA-Z]', a)
        if len(b) != 0:
            c = re.findall('[\u4e00-\u9fa5]', a)
            if len(c) == 0:
                data.iloc[i, 15] = '国外'
            else:
                data.iloc[i,15]='国内'
        else:
            data.iloc[i, 15] = '国内'
    return data

# 查看缺失值情况
def mis_value(data):
    data = data.replace('', np.nan)
    mis_val=data.isnull().sum()  # 计算出每一列有多少个缺失值,因为True=1,False=0
    mis_val_per=data.isnull().sum()/len(data)*100 # 计算每一列缺失值在该列占比多少
    mis_val_table=pd.concat([mis_val,mis_val_per],axis=1) #将两个Series横向拼接
    mis_val_table=mis_val_table.rename(columns={0:'缺失值个数',1:'缺失比例'})
    mis_pai=mis_val_table.sort_values(by='缺失比例',ascending=False) # 按缺失值比例进行排序
    return mis_pai

# 查看投资者所属项目
def invester_data(data, invester_top):
    l = invester_top['投资者'].to_list()
    ls = []
    for i in l:
        for x in range(len(data)):
            a = data.iloc[x, 8]
            if i in a:
                ls.append(x)
    ls = sorted(list(set(ls)))
    data = data.iloc[ls, :]
    return data

























