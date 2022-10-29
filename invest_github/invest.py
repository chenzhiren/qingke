import streamlit as st
from get_news import qingkespider
import pandas as pd
import data_clean
import money_change
from ind_change import ind_change
import data_analyse

st.sidebar.title('清科项目')
sidebar=st.sidebar.radio('',('资讯爬取和清洗','本周数据情况'))

if sidebar=='本周数据情况':
       data=pd.read_excel('qingke_sql.xlsx')
       data = data.rename(columns={0: 'company_name', 1: 'base', 2: 'found_time', 3: 'field', 4: 'business', 5:'round', 6: 'currency',
             7: 'money', 8: 'investers', 9: 'financing_time', 10: 'create_time', 11: 'pici', 12: 'reaal_money',
             13:'fenceng',14:'in_out',15:'id'})
       data_in=data[data['in_out']=='国内']
       st.header(data['create_time'][0]+'  第'+str(data['pici'][0])+'批次：总体数据情况')
       st.subheader('总数据量为：'+str(len(data))+'条')

       data_analyse.in_out_scale(data)

       data_analyse.topfive_industry(data)

       st.subheader('国内数据情况')
       data_analyse.guonei(data)
