import streamlit as st
import pymysql
import pandas as pd
sql='select * from risk limit 10'
conn=pymysql.connect(host=st.secrets.mysql.host,
                     port=st.secrets.mysql.port,
                     user=st.secrets.mysql.user,
                     passwd=st.secrets.mysql.passwd,
                     database = st.secrets.mysql.database)
cur = conn.cursor()
cur.execute(sql)
data = cur.fetchall()
data=pd.DataFrame(data)
st.dataframe(data)

