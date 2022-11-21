import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import Map
from streamlit_echarts import st_pyecharts
import streamlit.components.v1 as component

def in_out_scale(data):
    data_in=len(data[data['in_out'] == '国内'])
    data_out=len(data[data['in_out'] == '国外'])
    bar=(Bar()
         .add_xaxis(['国内外公司数量'])
         .add_yaxis('国内',[data_in])
         .add_yaxis('国外',[data_out])
         .set_global_opts(title_opts=opts.TitleOpts(title="国内外数据比例")))
    st_pyecharts(bar)
    return

def topfive_industry(data):
    five=data['field'].value_counts().head()
    bar=(Bar()
         .add_xaxis(list(five.index))
         .add_yaxis('融资事件数量',five.values.tolist(),color='blue')
         .set_global_opts(title_opts=opts.TitleOpts(title="")))
    st_pyecharts(bar)
    return

# 金额字段质量情况
def guonei(data):
    data_in = data[data['in_out'] == '国内']
    l1_data = pd.DataFrame(data_in['fenceng'].value_counts())
    pie = (Pie()
           .add('', [list(z) for z in zip(l1_data.index.to_list(), l1_data['fenceng'].to_list())])
           .set_global_opts(title_opts=opts.TitleOpts(title="国内数据金额字段质量"))
           .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}\n 占比{d}%"))

           )
    st_pyecharts(pie)
    return

# 前5投资者
def top_investers(data):
    ls = data['investers'].to_list()
    new_ls = []
    for i in ls:
        if ',' in i:
            i = i.split(',')
            for x in i:
                x = x.replace("'", '').strip()
                new_ls.append(x)
        else:
            i = i.strip()
            new_ls.append(i)
    s1 = pd.Series(new_ls, index=[None for i in range(len(new_ls))]).value_counts()
    if '不公开的投资者' in s1.index:
        s1 = s1.drop('不公开的投资者')
    if '' in s1.index:
        s1 = s1.drop('')
    if '天使投资人' in s1.index:
        s1=s1.drop('天使投资人')
    s1=s1.head(5)
    #s2 = pd.DataFrame(s1).reset_index().rename(columns={'index': '投资者', 0: '投资次数'})
    investers=s1.index.tolist()
    num=s1.values.tolist()
    tree=(Bar()
           .add_xaxis(investers)
           .add_yaxis('投资公司数量',num,color='brown')
           .set_global_opts(title_opts=opts.TitleOpts(title="前5投资机构"),
                            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15))))
    st_pyecharts(tree)
    return

# 地理位置分布情况
def weizhi(data):
    l1_data = pd.DataFrame(data['base'].value_counts())
    c=(Map()
       .add('投资事件数量', [list(z) for z in zip(l1_data.index.to_list(),l1_data['base'].to_list())],"china-cities")
       .set_global_opts(title_opts=opts.TitleOpts(title="Map-中国地图（带城市）"),
                        visualmap_opts=opts.VisualMapOpts(max_=25),)
       .render_embed()
       )
    component.html(c,height=500)
    return

