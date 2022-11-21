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
st.header('清科项目')
if st.button('开始爬取资讯'):
       qingkespider().run()
       st.success('爬取完成')

if st.button('清洗数据'):
       # 连接数据库
       conn = pymysql.connect(host='localhost', user='root', passwd='root', db='qingke', port=3306)
       # 游标
       cur = conn.cursor()
       # sql语句，获取所有原始数据
       sql='select * from company_origin_data2022 where pici>=40'
       sql2='select pici from company_origin_data2022 order by pici desc limit 1'
      # 执行sql语句
       cur.execute(sql)
       #获取sql语句的执行结果
       data=cur.fetchall()
       data = pd.DataFrame(data).reset_index()
       data = data.rename(columns={'index':'id',0: 'company_name', 1: 'base', 2: 'found_time', 3: 'field', 4: 'business', 5: 'round',
                    6: 'currency', 7: 'money',8: 'investers', 9: 'financing_time', 10: 'create_time', 11: 'pici'})

       # 去重和除括号
       data=data.drop_duplicates(subset=['company_name','base','found_time','field','business','round','currency','money','investers','financing_time'],keep='first')
       # 执行第二条sql语句
       cur.execute(sql2)
       num=cur.fetchall()[0][0]
       cur.close()  # 关闭游标
       conn.close()  # 断开连接
       data=data[data['pici']==num]
       data=data_clean.clean_1(data)


       # 统一金额为人民币计价
       data = money_change.qudanwei(data)
       data=money_change.currency_change(data)


       # 金额分层
       data=data_clean.fen_ceng(data)

       # 区分国内外公司
       data=data_clean.in_out(data)
       data['in_out']=data['in_out'].astype('str')

       # 统一行业
       data=ind_change(data)

       # 新建索引并存入数据库
       data=data.reset_index().drop(['index','id'],axis=1)
       data['id']=data.index
       engine=create_engine('mysql+pymysql://root:root@localhost:3306/qingke')
       data.to_sql('data_clean2022',con=engine,if_exists='append',index=False)
       st.success('数据清洗完成')

if st.button('展示当周数据情况'):
       conn = pymysql.connect(host='localhost', user='root', passwd='root', db='qingke', port=3306)
       cur = conn.cursor()
       sql = 'select * from data_clean2022 a where a.pici= \
                        (select a.pici  from data_clean2022 a order by a.pici desc limit 1)'
       cur.execute(sql)
       data = cur.fetchall()
       cur.close()  # 关闭游标
       conn.close()  # 断开连接
       data = pd.DataFrame(data)
       data = data.rename(
           columns={0: 'company_name', 1: 'base', 2: 'found_time', 3: 'field', 4: 'business', 5: 'round', 6: 'currency',
                    7: 'money', 8: 'investers', 9: 'financing_time', 10: 'create_time', 11: 'pici', 12: 'reaal_money',
                    13: 'fenceng', 14: 'in_out', 15: 'id'})
       mis_val=data_clean.mis_value(data)
       st.header(data['create_time'][0] + '  第' + str(data['pici'][0]) + '批次：总体数据情况')
       st.subheader('总数据量为：' + str(len(data)) + '行'+str(len(data.columns))+'列')
       st.dataframe(data.head())

       st.subheader('数据缺失值情况')
       st.dataframe(mis_val)


#if sidebar=='清科投融资数据分析':




