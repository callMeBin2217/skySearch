__author__='callMeBin'
#encoding=utf-8

'''
目标：利用天眼查查询公司的相关信息
'''

import requests
from bs4 import BeautifulSoup
import re
import codecs
import dataBaseTools


class skyEyesSearchContentGov(object):
	def __init__(self,url = r'https://www.tianyancha.com/company/409253885' ):
		self.BASE_URL = url
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
				'Host':'www.tianyancha.com',
				'Connection':'keep-alive',
				'Cache-Control':'max-age=0',
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Referer':'https://www.tianyancha.com/search?key=%E9%9F%B6%E5%85%B3',
				'Accept-Encoding':'gzip, deflate, sdch, br',
				'Accept-Language':'zh-CN,zh;q=0.8',
				#'Cookie':'aliyungf_tc=AQAAAHmj61ioogEAnCcP2vYdkAKxojqQ; csrfToken=3nEJ94JQJWO7qK2YsWJikj27; TYCID=c8216b7083db11e89c00e9be8f48d4f7; undefined=c8216b7083db11e89c00e9be8f48d4f7; ssuid=974676856; token=941f17a186b9459b8426a982bbbaa785; _utm=613873172ed24a1fa7e297039b2d6309; RTYCID=2cc9d3fa3a0b43c1a27d651ea5270a7b; bannerFlag=true; tyc-user-info=%257B%2522isExpired%2522%253A%25220%2522%252C%2522claimDetailLevel%2522%253A%252220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTExNTg0ODQzNSIsImlhdCI6MTUzMTc5NzA5MCwiZXhwIjoxNTQ3MzQ5MDkwfQ.hPO5Hhb5O3HmNLkiBzBEPJMgBWboBGWeYxl03OwSQI1RtXtxhNMpFfnXlS-RBRG0sGK18ge_jTqZN8H_BLHixw%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522surday%2522%253A%2522361%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%252229%2522%252C%2522mobile%2522%253A%252215115848435%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTExNTg0ODQzNSIsImlhdCI6MTUzMTc5NzA5MCwiZXhwIjoxNTQ3MzQ5MDkwfQ.hPO5Hhb5O3HmNLkiBzBEPJMgBWboBGWeYxl03OwSQI1RtXtxhNMpFfnXlS-RBRG0sGK18ge_jTqZN8H_BLHixw; _ga=GA1.2.861720786.1531701302; _gid=GA1.2.483185215.1531701302; _gat_gtag_UA_122238368_3=1; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1531701300,1531701317,1531791124,1531793895; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1531797098'

			}
		self.tabelName = 'message'
		self.dbTool = dataBaseTools.dataBaseTool()
		print(self.BASE_URL)

	#返回页面内容
	def getPage(self):
		data = requests.get(self.BASE_URL,headers=self.headers)
		dataContent = str(data.content,'utf-8')
		#print(data.encoding)
		#print(str(data.content,'utf-8'))
		return dataContent

	#传入页面，筛选事业单位
	def getContentContent(self,dataContent):
		#初始化SOUP实例对象
		soup = BeautifulSoup(dataContent,'lxml')
		#选出公司名
		div_cname = soup.find('div',attrs={'class':'header'}).h1.get_text()
		print(div_cname)
		#选出联系电话
		div_tel = " "
		print(div_tel)
		#选出公司法人
		div_table = soup.find('div',attrs={'class':'block-data'}).find('table',attrs={'class':'table'})
		div_lawer = div_table.find('tbody').find('tr').find('td').get_text()
		print(div_lawer)
		#选出统一信用代码
		div_table2 = soup.find('div',attrs={'class':'block-data'}).find('table',attrs={'class':'table -striped-col'})
		div_code = div_table2.find('tbody').find('tr').find('td').next_sibling.next_sibling.next_sibling.get_text()
		print(div_code)
		#选出地址
		div_address = div_table2.find('tbody').find('tr').next_sibling.next_sibling.find('td').next_sibling.get_text()
		print(div_address)
		#保存到数据库
		insert_str =  "INSERT INTO "+self.tabelName+"(name,lawer,codeNum,telphone,address) VALUES('%s','%s','%s','%s','%s')"%(div_cname,div_lawer,div_code,div_tel,div_address)
		self.dbTool.execute_insert(insert_str)
	




def main():
	spider = skyEyesSearchContentGov(r'https://www.tianyancha.com/company/3097060877')
	spider.getContentContent(spider.getPage())
	#getPage(BASE_URL)


if __name__=='__main__':
	main()