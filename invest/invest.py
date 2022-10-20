import streamlit as st
from get_news import qingkespider
import pymysql
import pandas as pd
import data_clean
import money_change
from ssh import SSHTunnelForwarder

server=SSHTunnelForwarder(
       ssh_address_or_host=('192.168.0.107',22),
       ssh_username=Y7000,
       ssh_password=999555,
       remote_bind_address=('localhost',3306)
    
st.sidebar.title('清科项目')
sidebar=st.sidebar.radio('',('资讯爬取和清洗','本周数据情况'))
if sidebar=='资讯爬取和清洗':
   if st.button('开始爬取资讯'):
       qingkespider().run()
       st.success('爬取完成')

   if st.button('清洗数据'):
       # 连接数据库
       conn=pymysql.connect(host=st.secrets.mysql.host, user=st.secrets.mysql.user, passwd=st.secrets.mysql.password, database=st.secrets.mysql.database, port=server.local_bind_port)
       # 游标
       cur = conn.cursor()
       # sql语句，获取最新批次数据
       sql = 'select * from company_origin_data2022 a where a.pici= \
             (select a.pici  from company_origin_data2022 a order by a.pici desc limit 1)'
      # 执行sql语句
       cur.execute(sql)
       #获取sql语句的执行结果
       data=cur.fetchall()
       cur.close()  # 关闭游标
       conn.close()  # 断开连接
       data = pd.DataFrame(data)
       data = data.rename(columns={0: 'id', 1: 'company_name', 2: 'base', 3: 'found_time', 4: 'field', 5: 'business', 6: 'round',
                    7: 'currency', 8: 'money',9: 'investers', 10: 'financing_time', 11: 'create_time', 12: 'pici'})

       # 去重和除括号
       data=data.drop_duplicates(subset=['company_name','base','found_time','field','business','round','currency','money','investers','financing_time'],keep='last')
       data=data_clean.clean_1(data)

       # 统一金额为人民币计价
       data=money_change.currency_change(data)

       # 金额分层
       data=data_clean.fen_ceng(data)
       #st.write(data.columns)

       # 区分国内外公司
       data=data_clean.in_out(data)
       data['地区']=data['地区'].astype('str')
       st.success('数据清洗完成')
       st.write(data['create_time'][0],'第'+str(data['pici'][0])+'批次：数据情况')
       st.write('总数据量为：'+str(len(data)))
       st.write(f'国内数据：{len(data[data["地区"] == "国内"])}')
       st.write(f'国外数据：{len(data[data["地区"] == "国外"])}')
