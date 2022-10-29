import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

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
         .set_global_opts(title_opts=opts.TitleOpts(title="融资事件前五行业")))
    st_pyecharts(bar)
    return


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