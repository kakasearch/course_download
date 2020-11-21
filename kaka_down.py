#写一个下载器，功能：自定义headers,cookie,session,不要重复下载，多线程下载

import threading
import requests
import re,os
import urllib.parse
from contextlib import closing
def  download_session(session,down_urls='',down_names='',headers='',path='./download/'):
	if not os.path.exists(path):
          os.makedirs(path)
	try:
		for i in range(len(down_urls)):
			if headers:
				with closing(requests.get(url=down_urls[i], allow_redirects=True,verify=False, stream=True)) as r:
					if not down_names[i]:#为空
						try:
							ame = re.findall(r'filename=".*"',r.headers['Content-Disposition'])[0]
							name = urllib.parse.unquote(name)
						except:
							name=down_urls[i].split('/')[-1]
					elif '.' not in down_names[i]:#没有后缀
						name = down_names[i]+name.split('.')[-1]
					else:
						name=down_names[i]
					#write file
					with open(path+name,'wb')as f:
						for chunk in r.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
					with open('./downlog.txt','a+',encoding='utf-8')as f:
						f.write(down_urls[i]+'\n')
					print('download success',name)
			else:
				with closing(requests.get(url=down_urls[i], verify=False, stream=True)) as r:
					#parse name
					if not down_names[i]:#为空
						try:
							ame = re.findall(r'filename=".*"',r.headers['Content-Disposition'])[0]
							name = urllib.parse.unquote(name)
						except:
							name=down_urls[i].split('/')[-1]
					elif '.' not in down_names[i]:#没有后缀
						name = down_names[i]+name.split('.')[-1]
					else:
						name=down_names[i]
					#write file
					with open(path+name,'wb')as f:
						for chunk in r.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
					with open('./downlog.txt','a+',encoding='utf-8')as f:
						f.write(down_urls[i]+'\n')
					print('download success',name)
	except:
		with open('./down_err0r.txt','a+',encoding='utf-8')as f:
						f.write(down_urls[i]+'\n')

#多线程分发
def fromsession(session,urls=[],outs=[],thread_num=1,headers='',path='./download/'):
	uls_len = len(urls)
	outs_len =len(outs)
	thread_max = 20
	if uls_len!=outs_len:
		print('urls与outs不对应')
		print(urls)
		print(outs)
		exit()
	if thread_num > thread_max:
		thread_num = thread_max
	elif thread_num <= 0:
		thread_num = 1
	else:#小于线程数时，一个线程一个
		thread_num=uls_len
	#去掉下载过的
	try:
		with open('./downlog.txt',encoding='utf-8')as f:
			done = f.read()
	except:
		done=''
	for i in range(uls_len):
		if urls[i] in done:
			del(urls[i])
			del(outs[i])

	#按线程数切块
	down_names = [[]*thread_num]
	down_urls=[[]*thread_num]#初始化空[[],[],[]]
	for i in range(len(urls)):#分发url到各自线程中
		#num = i%thread_num
		down_urls[i]+=[urls[i]]
		down_names[i]+=[outs[i]]
	
	#开始下载
	if not os.path.exists(path[:-1]):
		os.makedirs(path)
	obj_list = []
	for i in range(thread_num):
		print('downloading',down_names[i])
		t1 = threading.Thread(target=download_session,args=(session,down_urls[i],down_names[i],headers,path))
		t1.start()
		obj_list.append(t1)
	for t in obj_list:
		t.join()

