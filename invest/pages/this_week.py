import streamlit as st
from get_news import qingkespider
import pymysql
import pandas as pd
import data_clean
import money_change
from sqlalchemy import create_engine
from ind_change import ind_change
import data_analyse
import numpy as np


#取出最新一批次数据
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='qingke', port=3306)
cur = conn.cursor()
sql = 'select * from data_clean2022 a where a.pici= \
          (select a.pici  from data_clean2022 a order by a.pici desc limit 1)'
cur.execute(sql)
data = cur.fetchall()
cur.close()  # 关闭游标
conn.close()  # 断开连接
data=pd.DataFrame(data)
data = data.rename(columns={0: 'company_name', 1: 'base', 2: 'found_time', 3: 'field', 4: 'business', 5:'round', 6: 'currency',
      7: 'money', 8: 'investers', 9: 'financing_time', 10: 'create_time', 11: 'pici', 12: 'reaal_money',
      13:'fenceng',14:'in_out',15:'id'})
data_in=data[data['in_out']=='国内']
data_out=data[data['in_out']=='国外']

st.header('清科投融资数据分析')

data_analyse.in_out_scale(data)

st.subheader('国内数据情况')
# 前五行业
data_analyse.topfive_industry(data_in)
# 前五投资人
data_analyse.top_investers(data_in)
# 地理分布
data_analyse.weizhi(data_in)

st.subheader('国外数据情况')
# 前五行业
data_analyse.topfive_industry(data_out)
# 前五投资人
data_analyse.top_investers(data_out)