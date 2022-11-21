import requests
import random
from user_agent import USER_AGENT_LIST
from lxml import etree
import pymysql
import datetime
import re
from bs4 import BeautifulSoup
import time

# 连接数据库
conn=pymysql.connect(host='localhost',user='root',passwd='root',db='qingke',port=3306)
# 游标
cur=conn.cursor()
# 获取批次
sql='select pici from company_origin_data2022 order by company_origin_data2022.pici desc limit 1'
cur.execute(sql)
pici=int(cur.fetchall()[0][0])+1


# 定义一个爬取类
class qingkespider(object):
    # 定义初始化，包括原始连接地址，浏览器伪装
    def __init__(self):
        self.url='https://vc.pedaily.cn/invest/'
        self.headers={'User-Agent':random.choice(USER_AGENT_LIST)}
        self.pici=pici

    # 用request包请求网址，并获取网页内容
    def send_request(self,j):
        new_url=self.url+'p'+str(j)  # 拼接网页地址
        response=requests.get(url=new_url,headers=self.headers)  # 填写请求参数
        data=response.content.decode('utf-8') # 解析网页内容
        result=etree.HTML(data)  # 将字符串文字转换为 元素对象，再使用xpath语法
        return result  # 返回结果

    # 解析网页内容
    def parse_data(self,result,i):
        pro={}
        investlist=result.xpath('.//div[@class="box-list invest-list"]/div[@id="inv-list"]/dl')
        # 获取公司名称
        pro['name'] = investlist[i].xpath('./dt[@class="t"]/div[@class="txt"]/span[@class="block"]/text()')[0]
        # 获取公司地址
        base = investlist[i].xpath('./dt/a')[1].xpath('./text()')
        if len(base) != 0:
            pro['base'] = base[0]
        else:
            pro['base'] =''
        # 获取公司创立时间和主营业务
        detail=investlist[i].xpath('./dt[@class="t"]/div[@class="txt"]/a/@href')[0] # 获取公司详情页地址
        #durl='https://vc.pedaily.cn/'+detail  # 拼接详情页连接
        dresponse = requests.get(url=detail, headers=self.headers)
        ddata = dresponse.content.decode('utf-8')
        #print(ddata)
        pattern = re.compile('<span><i class="iconfont icon-clock"></i>(.*)</span>') #用正则匹配出创立时间
        found_time = pattern.findall(ddata)
        if len(found_time) != 0:
               pro['found_time'] = found_time[0]
        else:
            pro['found_time']=''
        # 获取公司所属行业
        pro['field'] = investlist[i].xpath('./dt/a')[0].xpath('./text()')[0]
        # 获取公司主营业务
        # 用BeautifulSoup匹配出主营业务
        soup = BeautifulSoup(ddata, 'lxml')
        pro['business'] = soup.select('.detail-header .detail-header-desc')[0].get_text().strip()
        # 获取公司融资轮次
        pro['round'] = investlist[i].xpath('./dt')[3].xpath('./text()')[0]
        # 获取公司融资金额
        pro['money'] = investlist[i].xpath('./dt')[3].xpath('./span/text()')[0]
        currency=['人民币','美元','欧元','英镑']
        for x in currency:
            if x in pro['money']:
                 pro['currency'] = x
                 break
            else:
                 pro['currency']= '暂不处理'
        # 获取投资机构名单
        ls = []
        investers = investlist[i].xpath('./dt')[5].xpath('./b')
        for x in range(len(investers)):
            a = investers[x].xpath('./text()')
            if len(a) != 0:
                ls.append(a[0])
            else:
                a = investers[x].xpath('./a/text()')
                ls.append(a[0])
        pro['investers'] = ls

        # 获取公式融资时间
        pro['financing_time'] = investlist[i].xpath('./dt')[4].xpath('./text()')[0]
        print(pro)
        return pro

    def save_data(self,pro):
        name=pro["name"]
        base=pro["base"]
        found_time=pro["found_time"]
        field=pro["field"]
        business=pro["business"]
        round=pro["round"]
        currency=pro["currency"]
        money=pro["money"]
        investers=pro["investers"]
        financing_time=pro["financing_time"]
        time=datetime.date.today()
        pici=self.pici
        sql2='insert into company_origin_data2022 values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.\
            format(name,base,found_time,field,business,round,currency,money,investers,financing_time,str(time),pici)
        cur.execute(sql2)
        conn.commit()

    def run(self):
        x=0
        for j in range(1,11):
          t=0
          for i in range(1,21):
                 result=self.send_request(j)
                 pro=self.parse_data(result,i)
                 #self.save_data(pro)
                 t+=1
          print(t)
          x+=1
          print(x)

        cur.close()  # 关闭游标
        conn.close()  # 断开连接

qingkespider().run()



