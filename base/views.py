from django.shortcuts import render
from crawler.models import pttdata
import csv
import numpy as np
import datetime
import re


def change_to_table(pos_dict_temp):

	pos_dict=dict()
	temp_keyword=[]
	list1=[]
	temp=[]
	if len(pos_dict_temp)==1:
		i=0
		temp_keyword.append(pos_dict_temp[i]["keyword"])
			#dict1={"title":pos_dict[i]['title'],"date":pos_dict[i]['date'],"href":pos_dict[i]['href'],"keyword":temp_keyword}
		dict1={"title":pos_dict_temp[i]["title"]}
		dict2={"date":pos_dict_temp[i]["date"]}
		dict3={"href":pos_dict_temp[i]["href"]}
		dict4={"keyword":temp_keyword}
		list1=[dict1,dict2,dict3,dict4]
		temp_keyword=[]
		temp.append(list1)
		list1=[]
	for i in range(len(pos_dict_temp)-1):

			
		if pos_dict_temp[i]["title"]==pos_dict_temp[i+1]["title"]:
			temp_keyword.append(pos_dict_temp[i]["keyword"])
		else:
			temp_keyword.append(pos_dict_temp[i]["keyword"])
			#dict1={"title":pos_dict[i]['title'],"date":pos_dict[i]['date'],"href":pos_dict[i]['href'],"keyword":temp_keyword}
			#print(pos_dict_temp[i]["title"],temp_keyword)
			dict1={"title":pos_dict_temp[i]["title"]}
			dict2={"date":pos_dict_temp[i]["date"]}
			dict3={"href":pos_dict_temp[i]["href"]}
			dict4={"keyword":temp_keyword}
			list1=[dict1,dict2,dict3,dict4]
			temp_keyword=[]
			temp.append(list1)
			list1=[]
		if i ==len(pos_dict_temp)-2:
			a=len(pos_dict_temp)-1
			temp_keyword.append(pos_dict_temp[a]["keyword"])
			#dict1={"title":pos_dict[i]['title'],"date":pos_dict[i]['date'],"href":pos_dict[i]['href'],"keyword":temp_keyword}
			dict1={"title":pos_dict_temp[a]["title"]}
			dict2={"date":pos_dict_temp[a]["date"]}
			dict3={"href":pos_dict_temp[a]["href"]}
			dict4={"keyword":temp_keyword}
			list1=[dict1,dict2,dict3,dict4]
			temp_keyword=[]
			temp.append(list1)
			list1=[]
	pos_dict=temp
	return pos_dict

def pos_table(request):
	pos_dict=request.session['pos_dict'] 
	pos_dict=change_to_table(pos_dict)
	return render(request, 'table.html',locals())

def neg_table(request):
	neg_dict=request.session['neg_dict'] 
	pos_dict=change_to_table(neg_dict)
	return render(request, 'table.html',locals())


def neg_fin_table(request):
	neg_fin_dict=request.session['neg_fin_dict'] 
	pos_dict=change_to_table(neg_fin_dict)
	return render(request, 'table.html',locals())

def pos_fin_table(request):
	pos_fin_dict=request.session['pos_fin_dict'] 
	pos_dict=change_to_table(pos_fin_dict)

	return render(request, 'table.html',locals())


# Create your views here.
def new_trend(date):
	news_trend_count= dict()		#關鍵字趨勢的dict
	for one in date:
		if one in news_trend_count:
			news_trend_count[one] += 1
		else:
			news_trend_count[one] = 0
	return news_trend_count
	#print(news_trend_count)



	filter_data=[]	#提取情緒字典
	for i in range(len(title)):
		if title[i]!="None" and href[i]!="None":
			dict1={"title":title[i],"date":date[i],"href":href[i]}
			
			filter_data.append(dict1)


def sent_trend(title,content,date,href,sent_dict):
	sent_trend_count= dict()		#關鍵字趨勢 by date 的dict
	sent_text_count= dict()
	filter_data=[]

	for i in range(len(date)):
		temp=0
		for j in range(len(sent_dict)):
			if (sent_dict[j] in title[i] or sent_dict[j] in content[i])and len(sent_dict[j])>1:
				temp=1
				#print(sent_dict[j])
				dict1={"title":title[i],"date":date[i],"href":href[i],"keyword":sent_dict[j]}
				filter_data.append(dict1)
				if sent_dict[j] in sent_text_count : 	
					sent_text_count[sent_dict[j]] += 1
				elif sent_dict[j] not in sent_text_count: 
					sent_text_count[sent_dict[j]] =1

		if temp ==1:
			if date[i] in sent_trend_count: 	
				sent_trend_count[date[i]] += 1
			else:
				sent_trend_count[date[i]] =1
				
		elif temp==0:
			if date[i] in sent_trend_count: 	
				pass
			else:
				sent_trend_count[date[i]] =0

	return sent_trend_count,sent_text_count,filter_data


def company_count_function(company,title,content):

	company_count= dict()		#關鍵字趨勢的dict
	for one in company:
		for i in range(len(title)):
			if one in title[i] or one in content[i]:
				if one in company_count or one in company_count:
					company_count[one] += 1
					#print(one,title[i])
				else:
					company_count[one] = 1
			else:
				pass
	return company_count
	
def normalize(d, target=50):
    raw = sum(d.values())
    if raw==0:
    	raw=1
    if len(d)==1:
        target=10
    factor = target/raw
    return {key:value*factor for key,value in d.items()}

def sent_dict():
	#輸入情感字典
	with open('static/NTUSD/negatives整理.txt', mode='r', encoding='utf-8') as f:
		negs = f.readlines()
	with open('static/NTUSD/positives整理.txt', mode='r', encoding='utf-8') as f:
		poss = f.readlines()
	pos = []
	for i in poss:
		a=re.findall(r'\w+',i) 
		pos.extend(a)
	neg = []
	for i in negs:
		a=re.findall(r'\w+',i) 
		neg.extend(a)
	return pos,neg


def fin_dict():
	#輸入情感字典
	with open('static/NTUSD/negatives金融.txt', mode='r', encoding='utf-8') as f:
		negs = f.readlines()
	with open('static/NTUSD/positives金融.txt', mode='r', encoding='utf-8') as f:
		poss = f.readlines()
	pos_fin = []
	for i in poss:
		a=re.findall(r'\w+',i) 
		pos_fin.extend(a)
	neg_fin = []
	for i in negs:
		a=re.findall(r'\w+',i) 
		neg_fin.extend(a)
	return pos_fin,neg_fin

def all_company_name():
#輸入公司字典
	with open('static/NTUSD/all_company_name.txt', mode='r', encoding='utf-8') as f:
		temps = f.readlines()
	company = []
	for i in temps:
		a=re.findall(r'\w+',i) 
		company.extend(a)
	return company


def Fin_chart(title,content,pos_fin,neg_fin):#Financual Sentiment Chart
	pos_fin_count=0
	neg_fin_count=0
	for j in range(len(title)):
		for i in range(len(pos_fin)):
			if pos_fin[i] in title[j] or pos_fin[i] in content[j]:
				pos_fin_count=pos_fin_count+1
					#print(pos_fin[i],title[j])
	for j in range(len(title)):
		for i in range(len(neg_fin)):
			if neg_fin[i] in title[j] or  neg_fin[i] in content[j]:
				neg_fin_count=neg_fin_count+1
					#print(neg_fin[i],title[j])

	return pos_fin_count,neg_fin_count

def range_filter(dayrange,filter_title,filter_author,filter_content,filter_date,filter_href,filter_pushcount):
	tempday=datetime.date.today() 
	daylist=[]
	title=[]
	author=[]
	content=[]
	date=[]
	href=[]
	pushcount=[]

	z=0
	temp=0
	for j in range(dayrange):    			 #塞選二週的新聞
		
		someday = datetime.date.today()  #預設從當天開始算
		day=someday.strftime("%m/%d")


		tempday += datetime.timedelta(days = -1)
		daytemp=tempday.strftime("%m/%d")
		daylist.append(daytemp)   #14天的日期

		if j==0:
			temp ==1
		
		someday += datetime.timedelta(days = -z)
		day=someday.strftime("%m/%d")
		for i in range(len(filter_date)-1,-1,-1):
			if filter_date[i]==day:
			#	print("就是這天",day)
				title.append(filter_title[i])
				author.append(filter_author[i])
				content.append(filter_content[i])
				date.append(filter_date[i])
				href.append(filter_href[i])
				pushcount.append(filter_pushcount[i]) #把日期資料濾開
			else:
				temp=1
		if temp ==1:		
			#print("沒有這天",day)
			title.append("None")
			author.append("None")
			content.append("None")
			date.append(day)
			href.append("None")
			pushcount.append("None") #把日期資料濾開
			temp=0
		#print(title)
		z=z+1
		#print(someday.strftime("%m/%d"))
	return title,author,content,date,href,pushcount

def take_dic(a,number):
	n = number
	L = sorted(a.items(),key=lambda item:item[1],reverse=True)
	L = L[:n]
	#print(L)
	dictdata = {}
	for l in L:
		dictdata[l[0]] = l[1]
	#print(dictdata)
	return dictdata






# Create your views here.
def hello_view(request):

	search = request.POST.get('search', None)
	search = str(search)

	if search=="None":
		print('search=="None"')
		# search="新聞"
		return render(request, 'index.html', locals())
	else:
		all_data = pttdata.objects.all()
		alldata_title = []
		alldata_author = []
		alldata_content = []
		alldata_date = []
		alldata_href = []
		alldata_pushcount = []


		#a=all_data[1].title
		filter_title=[]
		filter_author=[]
		filter_content=[]
		filter_date=[]
		filter_href=[]
		filter_pushcount=[]

		for i in range(len(all_data)):
			alldata_title.append(all_data[i].title)
			alldata_author.append(all_data[i].author)
			alldata_content.append(all_data[i].content)

			temp=all_data[i].date.strftime("%m/%d")
			alldata_date.append(str(temp))
			alldata_href.append(all_data[i].href)
			alldata_pushcount.append(all_data[i].pushcount) #把新聞資料濾開


			if "新聞" in all_data[i].title:

				if "Re" in all_data[i].title or "Fw" in all_data[i].title:

					pass 
				elif search in all_data[i].title:
					filter_title.append(all_data[i].title)
					filter_author.append(all_data[i].author)
					filter_content.append(all_data[i].content)

					temp=all_data[i].date.strftime("%m/%d")
					filter_date.append(str(temp))
					filter_href.append(all_data[i].href)
					filter_pushcount.append(all_data[i].pushcount) #把新聞資料濾開


		#print(filter_date)


		

		#把全部的元素限制在過去14天
		title,author,content,date,href,pushcount=range_filter(14,filter_title,filter_author,filter_content,filter_date,filter_href,filter_pushcount)

		
		pos,neg=sent_dict()	#提取情緒字典
		pos_fin,neg_fin=fin_dict()	#提取金融字典
		company=all_company_name()	#提取公司字典

		news_trend_count=new_trend(date)  #make  Keyword Trend Chart   做出關鍵字趨勢圖
		#make  positive Keyword Trend Chart   做出正向關鍵字趨勢圖
		positive_trend_chart,pos_fin_text_count,pos_fin_dict=sent_trend(title,content,date,href,pos_fin)
		#make  Negative Keyword Trend Chart   做出負向關鍵字趨勢圖
		negative_trend_chart,neg_fin_text_count,neg_fin_dict=sent_trend(title,content,date,href,neg_fin)

		positive_trend_chart,pos_sent_text_count,pos_dict=sent_trend(title,content,date,href,pos)
		positive_trend_chart,neg_sent_text_count,neg_dict=sent_trend(title,content,date,href,neg)
		pos_sent_text_count=take_dic(pos_sent_text_count,10)
		neg_sent_text_count=take_dic(neg_sent_text_count,10)
		pos_fin_text_count=take_dic(pos_fin_text_count,10)
		neg_fin_text_count=take_dic(neg_fin_text_count,10)

		normlize_pos=normalize(pos_sent_text_count)
		normlize_neg=normalize(neg_sent_text_count)
		normlize_pos_fin=normalize(pos_fin_text_count)
		normlize_neg_fin=normalize(neg_fin_text_count)
		#print(pos_fin_dict)



		#make  Financial pie Chart  做出金融圓餅圖
		pos_fin_count,neg_fin_count=Fin_chart(title,content,pos_fin,neg_fin) 
		#make  Normal pie Chart  做出情緒圓餅圖
		pos_count,neg_count=Fin_chart(title,content,pos,neg) 
		#make  company Bubble  Chartny   做出泡泡圖  注意泡泡圖的資訊跟上面的都不一樣。是allata
		title,author,content,date,href,pushcount=range_filter(7,alldata_title,alldata_author,alldata_content,alldata_date,alldata_href,alldata_pushcount)
		company_count=company_count_function(company,title,content)
		stopword=["正文","大量","統一","材料","國產","聯發","台南"]
		for i in stopword:
			try:
				del company_count[i]
			except KeyError:
				pass
		company_rank=take_dic(company_count,10)


		request.session['pos_dict'] = pos_dict
		request.session['neg_dict'] = neg_dict
		request.session['pos_fin_dict'] = pos_fin_dict
		request.session['neg_fin_dict'] = neg_fin_dict
		#print(news_trend_count)
		return render(request, 'index.html', locals())
