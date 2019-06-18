import urllib.request
from bs4 import BeautifulSoup
import re
import time
def getWishList(doubanid='91835006'):
    firstpage='https://movie.douban.com/people/'+doubanid+'/wish?start=0&sort=time&rating=all&filter=all&mode=list'
    request=urllib.request.urlopen(url=firstpage)
    page=1
    print(f'第{page}页',request.reason)
    wish_list=[]
    soup=BeautifulSoup(request.read())
    for item in soup.find_all('a',href=re.compile("subject")):
        wish_list.append(item.string.replace(' ','').strip('\n'))
    while 1:
        try:
            NextPage='https://movie.douban.com'+soup.find(class_='next').link.get('href')
        except:
            break
        else:
            request=urllib.request.urlopen(url=NextPage)
            page+=1
            print(f'第{page}页',request.reason)
            soup=BeautifulSoup(request.read())
            for item in soup.find_all('a',href=re.compile("subject")):
                wish_list.append(item.string.replace(' ','').strip('\n'))
            time.sleep(0.5)
    fw=open(doubanid+'_Wish_List.txt','w',encoding='utf-8_sig')
    fw.write('中文名 / 原名 \n')
    for item in wish_list:
        fw.write(str(item)+'\n')

def TCappend(TC,titandcom):
    for i in range(len(titandcom)):
        title=titandcom[i].em.text
        date=titandcom[i](class_=re.compile('date'))[0].text
        try:
            star=titandcom[i](class_=re.compile('rat'))[0]['class'][0][6]
        except:
            star='Nah'
        try:
            comment=titandcom[i](class_=re.compile('comment'))[0].text
        except:
            comment='Nah'
        TC[title]=[date,star,comment]

def getSawList(doubanid='91835006'):
    firstpage='https://movie.douban.com/people/'+doubanid+'/collect'
    request=urllib.request.urlopen(url=firstpage)
    page=1
    print(f'第{page}页',request.reason)
    saw_dic={}
    soup=BeautifulSoup(request.read())
    tandc=soup.find_all(class_=['item'])
    TCappend(TC=saw_dic,titandcom=tandc)
    while 1:
        try:
            NextPage='https://movie.douban.com'+soup.find(class_='next').link.get('href')
        except:
            break
        else:
            request=urllib.request.urlopen(url=NextPage)
            page+=1
            print(f'第{page}页',request.reason)
            soup=BeautifulSoup(request.read())
            tandc=soup.find_all(class_=['item'])
            TCappend(saw_dic,titandcom=tandc)
            time.sleep(0.5)
    fw=open(doubanid+'_Watched_List.csv','w',encoding='utf-8_sig')
    fw.write('中文名/原名,标记日期,评分,短评\n')
    for title in saw_dic.keys():
        fw.write(title.replace(',','、').replace('，','、')+','+saw_dic[title][0]+\
                 ','+saw_dic[title][1]+','+saw_dic[title][2].replace(',','、').replace('，','、')+'\n')

def main():
    douid=input('请输入你的豆瓣id：')
    print('正在下载‘想看’清单,存储为'+douid+'_Wish_List.txt')
    getWishList(doubanid=douid)
    print('开始下载电影评分与短评,存储为'+douid+'_Watched_List.csv')
    getSawList(doubanid=douid)
    print('程序结束，有问题发:<jimsun6428@gmail.com>')

main()