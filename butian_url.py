#coding:utf-8
import MySQLdb
import re
import urllib
import urllib2
import time
values=[]
id=1
try:
	conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='butian',port=3306,charset='utf8')
	cur=conn.cursor()
	for page in range(1,89):
		time.sleep(4)     #360会对访问速率做限制，所以需要暂停几秒
		response=urllib2.urlopen("https://butian.360.cn/company/lists/page/%d"%page)
		html=response.read()
		match_name=re.findall('[0-9]">(.*)</a',html)
		html_replace=re.sub('20px;"></td','20px;">www.null.com</td',html)#有些厂商只有名字，没有域名，为了让厂商名字和域名一一对应，将为空的域名先设置为www.null.com，具体见第厂商页面第38
		match_url=re.findall("20px;\">(.*\..*)</td",html_replace)
		for num in range(0,len(match_url)):
			values=[]html_replace
			values.append((id,match_name[num],match_url[num]))
			cur.executemany('insert into company values(%s,%s,%s)',values)
			print id
			conn.commit()
			id+=1
	cur.close()
	conn.close()
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])
