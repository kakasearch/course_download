#获取课程代码，已获取完毕
#写一个下载器，功能：自定义headers,cookie,session,不要重复下载，多线程下载
#获取全部文件的下载url
#传递给下载器，修改保存代码，从url获取文件后缀



import swjtu_jw_login
import kaka_down
import requests
import re,os
from lxml import etree


login = swjtu_jw_login.login(username='你的学号',password='你的密码')
session = login.session

#查看课程资源
coures_name=[]
coures_code=[]#装配url
#with open('./jwcode.csv',encoding='utf-8') as f:
#	list_ = f.readlines()
list_ = ['钢结构设计原理,0171060']  ##############可在jwcode.csv或教务网资源下载页自行查看
for item in [x.split(',') for x in list_]:
	coures_name += [item[0]]
	coures_code += [item[1]]
#http://jwc.swjtu.edu.cn/vatuu/StudentTeachResourceAction?setAction=teachResource&courseCode=6335010&courseName=结构力学AⅠ 
for i in range(len(coures_code)):#3):#
	course_url='http://jwc.swjtu.edu.cn/vatuu/StudentTeachResourceAction?setAction=teachResource&courseCode={}&courseName={}'.format(coures_code[i],coures_name[i])
	headers={
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Referer': 'http://jwc.swjtu.edu.cn/vatuu/StudentTeachResourceAction?setAction=teachCourse',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
	}
	r = session.get(course_url,headers=headers)
	#print(r.text)
	if('未查找到相关数据'in r.text):
		continue
	else:
		trs = re.findall(r'td>\d+</td>.*?查看</a></td>',r.text.replace('\n',''))
		with open('download.txt','w+',encoding='utf-8') as f:
			f.write('')
		for tr in trs:
			resource={}
			tds = re.findall(r'<td>(.*?)</td>',tr.replace(' ',''))
			#resource['name']= tds[2]#资源的名字、类别、上传者、上传时间
			resource['class'] = tds[3]
			resource['from']= tds[6]
			resource['time']= tds[7]
			resource['id'] = re.findall(r'Id=(\w+)\"',tr)[0]
			newheaders={
			'Cache-Control': 'max-age=0',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			}
			detail_url='http://jwc.swjtu.edu.cn/vatuu/StudentTeachResourceAction?setAction=teachResourceView&resourceId='+resource['id']
			r = session.get(detail_url,headers=newheaders)
			name = re.findall(r'资源名称.*?#0EA33F">(.*?)</td>',r.text.replace('\n',''))[0]
			resource['name']=name.split('.')[0]
			ext = name.split('.')[-1]
			print(resource,ext)
			with open('download.txt','a+',encoding='utf-8') as f:
				download_url = 'http://jwc.swjtu.edu.cn/vatuu/StudentTeachResourceAction?setAction=downloadTeachResource&resourceId='+resource["id"]
				out_name = "{}_{}_{}_{}.{}".format(resource['name'],resource['class'],resource['from'],resource['time'],ext)
				f.write(download_url+','+out_name+"\n")

##链接爬取完毕，准备下载
down_url=[]
down_name = []
with open('./download.txt','r',encoding='utf-8') as f:
	list_ = f.readlines()
for item in [x.split(',') for x in list_]:
	down_url += [item[0]]
	down_name += [item[1][:-1]]

##传入下载列表，开始下载
kaka_down.download_session(session,down_url,down_name,headers)


