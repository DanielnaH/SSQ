# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:07:39 2016
Description: Information Collection of SSQ(shuang'se'qiu)
@author: Daniel
"""
import urllib2
from bs4 import BeautifulSoup
import os
import re

#get the web page source code
def get_page(href):   
  headers = {
             'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
            }  
  req=urllib2.Request(url=href,headers=headers)
  try:  
    post = urllib2.urlopen(req)  
  except urllib2.HTTPError,e:
    print e.code  
    print e.reason  
  return post.read()
  
  

#get the amount of pages of url
def get_page_num(url):
  num =0  
  page = get_page(url)  
  soup = BeautifulSoup(page)    
  strong = soup.find('td',colspan='7')  
  # print strong  
  if strong:  
    result = strong.get_text().split(' ')  
    # print result  
    list_num = re.findall("[0-9]{1}",result[1])  
    # print list_num  
    for i in range(len(list_num)):  
      num = num*10 + int(list_num[i])  
    return num  
  else:
    return 0  

#get the informations on each page
def get_text(url):  
  for list_num in range(1,get_page_num(url)):   #从第一页到第getPageNum(url)页  
    print list_num  #打印下页码  
    href = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_'+str(list_num)+'.html' #调用新url链接  
    # for listnum in len(list_num):  
    page = BeautifulSoup(get_page(href))  
    em_list = page.find_all('em')   #匹配em内容  
    div_list = page.find_all('td',{'align':'center'})   #匹配 <td align=center>这样的内容  
  
    #初始化n  
    n = 0  
    #将双色球数字信息写入num.txt文件  
    fp = open("num.txt" ,"w")  
    for div in em_list:  
      # emnum1 = div.get_text()  
      # print emnum1  
      text = div.get_text()  
      text = text.encode('utf-8')  
      #print title         
      n=n+1  
      if n==7:  
        text = text + "\n"  
        n=0  
      else:  
        text = text + ","  
      fp.write(str(text))  
        
    fp.close()  
  
    #将日期信息写入date.txt文件  
    fp = open("date.txt" ,"w")  
    for div in div_list:  
      text = div.get_text().strip('')  
      # print text  
      list_num = re.findall('\d{4}-\d{2}-\d{2}',text)  
      list_num = str(list_num[::1])  
      list_num = list_num[3:13]  
      if len(list_num) == 0:  
        continue  
      elif len(list_num) > 1:  
        fp.write(str(list_num)+'\n')  
        
    fp.close()  
          
    #将num.txt和date.txt文件进行整合写入hun.txt文件中  
    #格式如下：  
    #('2016-05-03', '09,12,24,28,29,30,02')  
    #('2016-05-01', '06,08,13,14,22,27,10')  
    #('2016-04-28', '03,08,13,14,15,30,04')  
    fp01 = open("date.txt","r")  
    a=[]  
    for line01 in fp01:  
      a.append(line01.strip('\n'))  
      # print a  
    fp01.close()  

    fp02 = open("num.txt","r")  
    b=[]  
    for line02 in fp02:  
      b.append(line02.strip('\n'))  
      # print b  
    fp02.close()  
  
    fp = open("hun.txt" ,"a")  
    for cc in zip(a,b): #使用zip方法合并  
      print cc  
      fp.write(str(cc) + '\n')  
    fp.close()  


url='http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'          
pageNum = get_page_num(url)     
print pageNum  
getpagetext = get_text(url)    
print getpagetext  