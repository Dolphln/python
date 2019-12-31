#coding:utf-8
import requests
import json
import re
import pymysql.cursors
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

scan_time = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
today = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d 00:00:01")

print scan_time
print today

connection = pymysql.connect(host='10.28.2.235', port=3306, user='xh_sec', password='', db='',
			charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

_search_type = ["repositories","code","commits"]
keyword = []

def reset_key():
	if scan_time == today:
		#在每天0点的时候将execute重置为no
		sql_execute_update = "update `git_code_key` set `execute`='no' where `key`='{0}'".format(key)
		cursor.execute(sql)
		connection.commit()
	else:
		pass

def get_key():
	sql = "select * from git_code_key"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
		# 因为github有每小时60次的限制，所以要指定定时任务，每4小时跑一次，如果关键词更多，可以指定2小时或3小时跑一次
			if row['execute'] =='yes':
				pass
			else:
				if len(keyword)==40:    #限制每次运行的时候只查询40次
					pass
				else:
					keyword.append(row['key'])  #通过keyword限制是否需要继续爬
	except:
		print "Error: unable to fecth data"

def get_url(key):
	git_url=[]
	commits_header={'Accept':'application/vnd.github.cloak-preview'}
	repositories_header={'Accept':'application/vnd.github.mercy-preview+json'}
	code_res=json.loads(requests.get("https://api.github.com/search/code?q=%s&access_token=" % key).text)
	commits_res=json.loads(requests.get("https://api.github.com/search/commits?q=%s&access_token=" % key,headers = commits_header).text)
	repositories_res=json.loads(requests.get("https://api.github.com/search/repositories?q=%s&access_token=" % key,headers = repositories_header).text)
	# print code_res
	#print repositories_res

	if len(code_res['items'])==0:
		pass
	else:
		for item in code_res['items']:
			git_url.append(item['html_url'])

	if len(commits_res['items'])==0:
		pass
	else:
		for item in commits_res['items']:
			git_url.append(item['html_url'])

	if len(repositories_res['items'])==0:
		pass
	else:
		for item in repositories_res['items']:
			git_url.append(item['html_url'])

	return git_url

def main():
	reset_key()
	get_key()
	all_code_url=[]
	url_sql="select code_url from git_code_search"
	cursor.execute(url_sql)
	exist_result=cursor.fetchall()

	for item in exist_result:
		all_code_url.append(item['code_url'])

	for key in keyword:
		time.sleep(10) #需要限制爬取速率
		#每跑一次，要将execute标记记成yes
		print key
		sql_execute_update = "update `git_code_key` set `execute`='yes' where `key`='{0}'".format(key)
		cursor.execute(sql_execute_update)
		connection.commit()

		crawl_result=get_url(key)
		for url in crawl_result:
			if url in all_code_url:  #判断是否在数据库里是否已经有记录了，all_code_url：数据库现在有的url
				pass
			else:
				sql = "INSERT INTO `git_code_search` (`vul_key`,`scan_time`,`code_url`,`white_black`,`remark`,`link_type`) VALUES ('{}','{}','{}','{}','{}','{}')".format(key,scan_time,url,'白名单','无影响','code')
				print sql
				cursor.execute(sql)
				connection.commit()

if __name__ == '__main__':
	main()