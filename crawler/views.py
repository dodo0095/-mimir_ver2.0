from django.shortcuts import render
# Create your views here.
import requests
import time
import re
from bs4 import BeautifulSoup
import csv
import datetime
from datetime import datetime
from crawler.models import pttdata

def check_repeat_data(date,author,title,content,href,score,all_data):
    temp=0

    for i in range(len(title)):
        for j in range(len(all_data)):
            if all_data[j].title==title[i]:
                print(all_data[j].title)  
                print("寫入失敗")
                temp=0
                break
            else:
                temp=1
        if temp==1:
            pttdata.objects.create(date=date[i],author=author[i],title=title[i],content=content[i],href=href[i],pushcount=score[i])
            temp=0

def crawler(request):

    return render(request, 'crawler.html', {
        'data': "Hello Django ",
    })




PTT_URL = 'https://www.ptt.cc'
#API_KEY = '26266720e9aa08a4477f6ed04c1404ec'

def change2content(soup):
    content = soup.find(id="main-content").text
    target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    #去除掉 target_content
    content = content.split(target_content)
    #print(content)
    #content = content[0].split(date)
    #print(content)
    #去除掉文末 --
    main_content = content[0].replace('--', '')
    #印出內文
    #print(main_content)
    return main_content
    
    
def change2time(soup):
    main_content = soup.find(id="main-content")
    metas = main_content.select('div.article-metaline')
    if metas==[]:
        date='Tue Aug 20 23:05:13 2019'
        pass
    else:
        date = metas[2].select('span.article-meta-value')[0].string
    return date

def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').text.strip() == date:  # 發文日期正確
            # 取得推文數
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)  # 轉換字串為數字
                except ValueError:
                    # 若轉換失敗，可能是'爆'或 'X1', 'X2', ...
                    # 若不是, 不做任何事，push_count 保持為 0
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div', 'author').text if d.find('div', 'author') else ''
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_url


def POST_crawl(request):

    print('取得今日文章列表...')
    current_page = get_web_page(PTT_URL + '/bbs/Stock/index.html')
    if current_page:
        articles = []  # 全部的今日文章
        author=[]
        content=[]
        title=[]
        href=[]
        date=[]
        score=[]
        today = time.strftime('%m/%d').lstrip('0') 

        current_articles, prev_url = get_articles(current_page, today)  # 目前頁面的今日文章
        while current_articles:  # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, today)
        print('共 %d 篇文章' % (len(articles)))
        # 已取得文章列表，開始進入各文章尋找發文者 IP


      
        for article in articles[:9999]:
            page=requests.get(PTT_URL + article['href'])
            soup = BeautifulSoup(page.text, 'html.parser')
            temp=change2time(soup)
            temp=datetime.strptime(temp, "%a %b %d %H:%M:%S %Y")
            temp=temp.strftime("%Y-%m-%d %H:%M")
            date.append(temp)    #時間
            author.append(article['author'])  #作者
            title.append(article['title'])    #標題
            temp=change2content(soup)
            content.append(temp)  #內文
            href.append(PTT_URL+article['href'])      #連結
            score.append(article['push_count']) #需推文
            total_article=len(score)


    all_data=pttdata.objects.all()
    temp=0
    check_repeat_data(date,author,title,content,href,score,all_data)

    return render(request, 'simple_crawl_result.html',locals())









def get_all_href(url):
    title_T=[]
    href_T=[]
    pushcount=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.title")
    results2 = soup.select("div.nrec")
    for i in range(len(results2)):
        if "刪除" in results[i].text:
            pass
        else:
            if results2[i].text=="":
                pushcount.append(0)
            elif results2[i].text=="爆":
                pushcount.append(100)   
            elif "X" in results2[i].text:
                pushcount.append(-100)
            else:
                pushcount.append(results2[i].text)
    
    for item in results:
        a_item = item.select_one("a")
        title = item.text
        if "刪除" in title:
            pass
        else:
            title_T.append(title.strip())
        if a_item:
          #  print(title, 'https://www.ptt.cc'+ a_item.get('href'))
            href_T.append('https://www.ptt.cc'+ a_item.get('href'))
    return title_T,href_T,pushcount

def changelist(array):
    temparray=[]
    for i in range(len(array)):
        for j in range(len(array[i])):
            temparray.append(array[i][j])
    return temparray
def change2content(soup):
    content = soup.find(id="main-content").text
    target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    #去除掉 target_content
    content = content.split(target_content)
    #print(content)
    #content = content[0].split(date)
    #print(content)
    #去除掉文末 --
    main_content = content[0].replace('--', '')
    main_content = content[0].replace('\n', '')
    #印出內文
    #print(main_content)
    return main_content
    
    
def change2_time_author(soup):
    main_content = soup.find(id="main-content")
    metas = main_content.select('div.article-metaline')
    if len(metas)==3:
        if metas==[]:
            date=0
            author=0
            pass
        else:
            date = metas[2].select('span.article-meta-value')[0].string
            author = metas[0].select('span.article-meta-value')[0].string
    else:
        date='Tue Aug 20 23:05:13 2019'
        author="NA"
    return date,author

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False



#這是爬以前文章
def POST_crawl2(request):

    start_page = request.POST.get('start_page', None)
    how_many_page = request.POST.get('how_many_page', None)
    how_many_page=int(how_many_page)
    print("開始爬取 第 ",start_page," 並往前",how_many_page," 頁")
    url="https://www.ptt.cc/bbs/Stock/index"+start_page+".html"

    title_T=[]
    href_T=[]
    pushcount_T=[]
    for page in range(0,how_many_page):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        btn = soup.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        title,href,pushcount=get_all_href(url = url)
        title_T.append(title)
        href_T.append(href)
        pushcount_T.append(pushcount)
        time.sleep(10)
    href=[]
    title=[]
    date=[]
    author=[]
    content=[]
    title=changelist(title_T)  #標題
    href=changelist(href_T)    #網址
    pushcount=changelist(pushcount_T) #推文數量
    score=pushcount

    for i in range(len(title)):
        page=requests.get(href[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        temp,temp2=change2_time_author(soup)
        if type(temp)==int:
            temp='Tue Aug 20 23:05:13 2019'
        elif is_contains_chinese(temp)==True:
            temp='Tue Aug 20 23:05:13 2019'
        else:
            pass
        temp=datetime.strptime(temp, "%a %b %d %H:%M:%S %Y")
        temp=temp.strftime("%Y-%m-%d %H:%M")
        date.append(temp)    #時間
        author.append(temp2) #作者
        temp3=change2content(soup)
        content.append(temp3)#內文

    total_article=len(score)
    print(len(date),len(author),len(title),len(content),len(href),len(pushcount))
    all_data=pttdata.objects.all()
    check_repeat_data(date,author,title,content,href,pushcount,all_data)


    return render(request, 'simple_crawl_result.html',locals())
