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
st.set_page_config(
    layout='wide'
)
#取出最新一批次数据
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='qingke', port=3306)
cur = conn.cursor()
sql = 'select * from data_clean2022'

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

st.header('2022清科投融资数据分析')

col1,col2,col3=st.columns([2,0.5,2])
with col1:
   st.write('最新投资事件')
   new_data=data[['company_name','field','investers']]
   st.dataframe(new_data.tail(5))
with col2:
    pass
with col3:
   st.write('国内外投资事件数量')
   data_analyse.in_out_scale(data)

a1,a2,a3=st.columns([2,0.5,2])
with a1:
    st.write('国内最多投资事件的前五行业')
    data_analyse.topfive_industry(data_in)
with a2:
    pass
with a3:
    st.write('国外最多投资事件的前五行业')
    data_analyse.topfive_industry(data_out)

