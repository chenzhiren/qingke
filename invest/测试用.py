import requests
import random
from user_agent import USER_AGENT_LIST
from lxml import etree
import pymysql
import datetime

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
        self.url='https://zdb.pedaily.cn/inv/'
        self.headers={'User-Agent':random.choice(USER_AGENT_LIST)}
        self.pici=pici
    # 用request包请求网址，并获取网页内容
    def send_request(self,i,j):
        ini_url=self.url+'p'+str(j)+'/'  # 拼接网页地址
        response=requests.get(url=ini_url,headers=self.headers)  # 填写请求参数
        data=response.content.decode('utf-8') # 解析网页内容
        data1=etree.HTML(data)  # 将字符串文字转换为 元素对象，再使用xpath语法
        num=data1.xpath('//div[@class="list-invest list-inv"]/ul/li')[i].xpath('./div[@class="top"]/a/@href')[0] # 获取关键参数
        url2='https://zdb.pedaily.cn'
        new_url=url2 + num  # 拼接新地址
        response2=requests.get(url=new_url,headers=self.headers)  # 请求新地址
        result=response2.content.decode('utf-8')  # 解析网页内容
        return result  # 返回结果

    # 解析网页内容
    def parse_data(self,result):
        pro={}
        result1 = etree.HTML(result)
        # 获取公司名称
        pro['name'] = result1.xpath('//div[@class="zdb-top"]/div[@class="main vc-top"]/div[@class="box-fix-l"]/div[@class="info"]/h1/text()')
        if len(pro['name'])==0:
           pro['name']=''
        else:
           pro['name'] = result1.xpath('//div[@class="zdb-top"]/div[@class="main vc-top"]/div[@class="box-fix-l"]/div[@class="info"]/h1/text()')[0]
        # 获取公司地址
        pro['base'] = result1.xpath('//div[@class="zdb-top"]/div[@class="main vc-top"]/div[@class="box-fix-l"]/div[@class="info"]/ul/li/text()')[0]
        # 获取公司创立时间
        pro['found_time'] = result1.xpath('//div[@class="zdb-top"]/div[@class="main vc-top"]/div[@class="box-fix-l"]/div[@class="info"]/ul/li/text()')[2]
        # 获取公司所属行业
        pro['field'] = result1.xpath('//div[@class="zdb-top"]/div[@class="main vc-top"]/div[@class="box-fix-l"]/div[@class="info"]/ul/li/text()')[3]
        # 获取公司主营业务
        pro['business'] = result1.xpath('//div[@class="detail main"]/div[@class="box-fix-l"]/p/text()')
        if len(pro['business']) == 0:
            pro['business'] = result1.xpath('//div[@class="detail main"]/div[@class="box-fix-l"]/div/text()')
        # 获取公司融资轮次
        pro['round'] = result1.xpath('//div[@class="detail main"]/div[@class="box-fix-l"]/div[@class="box-plate index-zdb box-zdblist"]/'
                       'div[@class="list-invest"]/ul/li')[0].xpath('./div[@class="info"]/span[@class="r"]/text()')
        # 获取公司融资币种
        pro['currency'] = result1.xpath('//div[@class="detail main"]/div[@class="box-fix-l"]/div[@class="box-plate index-zdb box-zdblist"]/'
                       'div[@class="list-invest"]/ul/li')[0].xpath('./div[@class="info"]/span[@class="d"]/text()')
        # 获取公司融资金额
        pro['money'] = result1.xpath('//div[@class="detail main"]/div[@class="box-fix-l"]/div[@class="box-plate index-zdb box-zdblist"]/'
                       'div[@class="list-invest"]/ul/li')[0].xpath('./div[@class="info"]/span[@class="m"]/text()')
        # 获取投资机构名单
        invester = result1.xpath(
            '//div[@class="detail main"]/div[@class="box-fix-l"]/div[@class="box-plate index-zdb box-zdblist"]/'
            'div[@class="list-invest"]/ul/li')[0].xpath('./div[@class="group"]/a/text()')
        invester2 = result1.xpath(
            '//div[@class="detail main"]/div[@class="box-fix-l"]/div[@class="box-plate index-zdb box-zdblist"]/'
            'div[@class="list-invest"]/ul/li')[0].xpath('./div[@class="group"]/span/text()')
        for s in invester2:
            if len(s) > 1:
                invester.append(s)
        pro['investers'] = invester

        # 获取公式融资时间
        pro['financing_time'] = result1.xpath(
            '//div[@class="detail main"]/div[@class="box-fix-l"]/div[@class="box-plate index-zdb box-zdblist"]/'
            'div[@class="list-invest"]/ul/li')[0].xpath('./div[@class="date"]/text()')[0]
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
        for j in range(1,100):
          t=0
          for i in range(0,24):

                 result=self.send_request(i,j)
                 pro=self.parse_data(result)
                 self.save_data(pro)
                 t+=1

          print(t)
          x+=1
          print(x)
        cur.close()  # 关闭游标
        conn.close()  # 断开连接
qingkespider().run()



