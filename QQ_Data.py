#爬取需要的数据
import json
import os
from QQ_clean import filter_tags
import pandas as pd

class get_Data():
	def __init__(self,g_tk,session,qzonetoken,fri_id,usr):
		self.g_tk = g_tk
		self.session = session
		self.qzonetoken = session
		self.fri_id = fri_id
		self.usr = usr
		self.headers = {
			'authority': 'user.qzone.qq.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
		}

	'''	#判断好友空间是否可以访问
	def enter(self):
		enter_url = "https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/main_page_cgi?uin=" + str(self.fri_id) + "&param=3_1455574093_0|8_8_2016969619_1_1_0_1_1|15|16&g_tk=" + str(self.g_tk) + "&qzonetoken=" + str(self.qzonetoken)

		r = self.session.get(enter_url)
		data = json.loads(r.text.encode('utf-8'))
		if data:
			return True

		else:
			return False'''

	#下载相册
	def download(self):
		pic_url = "https://mobile.qzone.qq.com/list?qzonetoken="+str(self.qzonetoken)+"&g_tk="+str(self.g_tk)+"&format=json&list_type=album&action=0&res_uin="+str(self.fri_id)+"&count=50"
		r = self.session.get(pic_url)
		data = json.loads(r.text.encode('utf-8'))
		#print(data)
		#print(self.qzonetoken)

		for album in data['data']['vFeeds']:
			na = album['pic']['albumname']
			Id = album['pic']['albumid']
			num = album['pic']['albumnum']
			print('相册名:'+str(na))
			print('相册id:'+str(Id))
			print('照片数量:'+str(num))

			#读取当前相册
			pho_url = "https://h5.qzone.qq.com/webapp/json/mqzone_photo/getPhotoList2?qzonetoken="+str(self.qzonetoken)+"&g_tk="+str(self.g_tk)+"&uin="+str(self.fri_id)+"&albumid="+str(album['pic']['albumid'])+"&ps=0"
			res = self.session.get(pho_url)
			photos_data = json.loads(res.text.encode('utf-8'))
			#print(photos_data)

			#判断相册是否上锁
			b = str(photos_data['message'])
			if b == '答案错误，请重新输入':
				print('该死的,相册竟然上锁了,真小气...')
				print('==========')

			else:
				items = []
				items = photos_data['data']['photos']
				for t in items:
					pho_list = []
					pho_list = photos_data['data']['photos'][t]
					for p in pho_list:
						nam = p['picname']
						Url = p['1']['url']
						print('图片名:'+ str(nam) +'，url:'+ str(Url))

	#爬取留言板
	def note(self):
		start = 0#c初始第一页为0
		limit = 10#每加10就加一页
		count = 0#用于计数
		f = open('note.txt', 'w', encoding='UTF-8')
		#url,不要填错,不要少东西,要自己找到这个链接把s=换到下面,否则留言显示不全
		url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com' \
          '/cgi-bin/new/get_msgb?uin=%s&hostUin=%s&start=0' \
          '&s=0.31334290730849135&format=jsonp&num=%s&inCharset=utf-8' \
          '&outCharset=utf-8&g_tk=%s&qzonetoken=%s&g_tk=%s' % (self.usr, self.fri_id, limit, self.g_tk, self.qzonetoken, self.g_tk)
		
		r = self.session.get(url)
		text = r.text
		#去掉返回json中的_CallBack以及后面的); 才能格式化为json
		#print(r.text)
		text = text[10:-2]
		js = json.loads(text)
		#print(js)
		total = js['data']['total']
		UinList = [None]*total
		NmaeList = [None]*total
		ContentList = [None]*total
		while start<total + 10:
			note_url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com' \
          '/cgi-bin/new/get_msgb?uin=%s&hostUin=%s&start=%s' \
          '&s=0.31334290730849135&format=jsonp&num=%s&inCharset=utf-8' \
          '&outCharset=utf-8&g_tk=%s&qzonetoken=%s&g_tk=%s' % (self.usr, self.fri_id, start, limit, self.g_tk, self.qzonetoken, self.g_tk)
			r = self.session.get(note_url)
			text = r.text
			#去掉返回json中的_CallBack以及后面的); 才能格式化为json
			text = text[10:-3]
			j = json.loads(text)
			start = start + 10
			commentList = j['data']['commentList']
			#循环遍历每页的评论
			for comList in commentList:
				#print(len(comList))
				#secret用于判别留言是否所有人可见
				secret = comList['secret']
				#control = comList['ubbContent']
				if secret == 0:
					com_Id = comList['id']#留言ID
					com_time = comList['pubtime']##留言时间
					com_nick = comList['nickname']#昵称
					com_uin = comList['uin']#QQ号
					#留言内容,还有一个ubbContent,选用htmlContent是已经对数据进行清洗
					com_content = comList['htmlContent']
					#QQ号表和昵称表,是完整的,可用来操作计数
					UinList[count] = com_uin
					NmaeList[count] = com_nick
					ContentList[count] = filter_tags(com_content)
					print('==========')
					count = count + 1
					#写入note.txt,这里使用的是htmlContent,便于处理,数据清洗
					f.write(filter_tags(str(count) + '  --' + str(comList['htmlContent'])) + '\n\n')
					#f.write('正在爬取第 %d 页, 第 %d 条留言...'%(start/10,count) + '留言一共有 %d'% int(total) + '\n')
					print('正在爬取第 %d 页, 第 %d 条留言...'%(start/10,count) + '留言一共有 %d'% int(total))
					print('留言ID为:  ' + str(com_Id))	
					print(str(com_time) + ':\n' +'留言者:  ' +  str(com_nick) + '--QQ号码:  ' + str(com_uin) + ':')
					print('留言内容为:')
					print(str(com_content))
					print('----------')
					#循环遍历回复表
					for replyList in comList['replyList']:
						rep_uin = replyList['uin']#回复者QQ
						rep_nick = replyList['nick']#回复者昵称
						rep_content = replyList['content']#回复内容
						print('回复者:  ' +  str(rep_nick) + '--QQ号码--' + str(rep_uin) + ':')
						print('回复如下:  ')
						print(str(rep_content))


				else:
					print('==========')
					count = count + 1
					print('正在爬取第 %d 页, 第 %d 条留言...'%(start/10,count) + '留言一共有 %d'% int(total))
					print('妈呀~( ⊙ o ⊙ )~,这位好友的留言竟然不让你看...')

		print('==========')		
		print('留言爬取完毕,如果你发现留言数量不够,这不能怪我哦,要怪就怪你的好友把留言藏起来了哦')
		print('==========')
		#向Info()中传入两个完整表
		self.Info(UinList, NmaeList)
		data = pd.DataFrame(ContentList)
		data.to_csv('note.csv',header = '留言', index = False, mode = 'w')
		
	#对留言进行统计,估计你和我一样对留言最多的那个qq很感兴趣~
	def Info(self, UinList, NmaeList):
		n = len(UinList)
		NickUinDict = {}
		#词典保存qq和昵称的一一对应关系,不用来计数
		for i in range(0,n):
			NickUinDict[UinList[i]] = NmaeList[i]

		#set()函数对QQ表中每个qq出现的次数进行统计,但并未排序,而且myset中只存了次数没有存QQ号
		myset = set(UinList)
		i = 0
		Info_1 = {}#字典中每个QQ号及其出现次数一一对应
		for item in myset:
			#print("QQ号码: %d 出现 %d 次" %(item,UinList.count(item)))
			if UinList.count(item) >= 1:
				Info_1[item] = UinList.count(item)
				#利用dict()中的sorted()函数对Info_1进行排序,降序,且QQ和次数一一对应
				Info_2 = dict(sorted(Info_1.items(), key=lambda x: x[1], reverse=True))
				#Info_1 = sorted(Info_1.items,key = lambda item:item[1])
		

		Info_3 = {}#字典为昵称和出现次数一一对应,降序
		for Uid in Info_2:
			Info_3[NickUinDict[Uid]] = Info_2[Uid]

		self.print_Info(Info_2,Info_3)

	#输出留言模块
	def print_Info(self,Info_2,Info_3):
		print('以留言QQ及其留言次数降序输出为:')
		print(Info_2)
		print('==========')
		print(Info_3)


#将好友信息存起来
	def informations(self,informations_Dict):
		informations_url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin=' + str(self.fri_id) + '&vuin=' + str(self.usr) + '&fupdate=1&g_tk=' + str(self.g_tk)
	    r = self.session.get(informations_url)
	    text = r.text
	    text = text[10:-3]
	    js = json.loads(text)
	    print('informations_url:	' + informations_url)
	    #print('QQ:  ' + fri_id + '  详细信息如下:  ' + text)
	    control = js['message']
	    if control == '获取成功':
	        i = 0
	        informations_data = js['data']
	        uin = informations_data['uin']#--QQ号
	        nickname = informations_data['nickname']#--昵称
	        spacename = informations_data['spacename']#--空间昵称
	        desc = informations_data['desc']#--描述
	        signature = informations_data['signature']#--签名
	        sex_select = informations_data['sex']#--性别-1-男,2-女
	        if sex_select == 1:
	            sex = '男'
	        elif sex_select == 2:
	            sex = '女'
	        else:
	            sex = '不明'
	        age = informations_data['age']#--年龄周岁
	        birthyear = informations_data['birthyear']#--出生年份
	        birthday = informations_data['birthday']#--出生日期
	        birth = str(birthyear) + '-' + str(birthday)#--出生年月日
	        blood = informations_data['bloodtype']#--血型--1-A,2-B,3-O,4-AB,5-其他
	        if blood == 1:
	            bloodtype = 'A'
	        elif blood == 2:
	            bloodtype = 'B'
	        elif blood == 3:
	            bloodtype = 'O'
	        elif blood == 4:
	            bloodtype = 'AB'
	        else:
	            bloodtype = '其他'
	        address_now = informations_data['country'] + '-' + informations_data['province'] + '-' + informations_data['city']#现居地
	        address__past = informations_data['hco'] + '-' + informations_data['hp'] + '-' + informations_data['hc']#故居
	        marriage_select = informations_data['marriage']#--感情状况--0-None,1-单身,2-恋爱中,3-已订婚,4-已婚,5-分居,6-离异,7-保密
	        if marriage_select == 0:
	            marriage = '不明'
	        elif marriage_select == 1:
	            marriage = '单身'
	        elif marriage_select == 2:
	            marriage = '恋爱中'
	        elif marriage_select == 3:
	            marriage = '已订婚'
	        elif marriage_select == 4:
	            marriage = '已婚'
	        elif marriage_select == 5:
	            marriage = '分居'
	        elif marriage_select == 6:
	            marriage = '离异'
	        elif marriage_select == 7:
	            marriage = '保密'
	        else:
	            marriage = '不明'
	        company = informations_data['company']#--公司
	        #ptimestamp = informations_data['ptimestamp']#--时间戳
	        informations_desc = ['昵称/备注','空间昵称','空间描述','个性签名','性别','年龄(周岁)','出生年月日','血型','现居地','故居','感情状况','公司']
	        n = len(informations_desc)
	        informations_List = [nickname,filter_tags(spacename),filter_tags(desc),filter_tags(signature),sex,age,birth,bloodtype,address_now,address__past,marriage,company]
	        informations_Dict[self.fri_id] = informations_List
	        print(informations_Dict)
	        print('QQ号为:  ' + str(self.fri_id) + '的好友详细信息如下:')
	        for i in range(0,n):
	            print(informations_desc[i] + ': ' + str(informations_List[i]))

	    else:
	        print('权限不足,无法获取好友信息')
