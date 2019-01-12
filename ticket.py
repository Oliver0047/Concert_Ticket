# -*- coding: utf-8 -*-
#autor:Oliver0047
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep
import re
from tkinter import *
import time

damai_url="https://www.damai.cn/"
login_url="https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
class Concert(object):
    def __init__(self,name,date,price,place):
        self.name=name
        self.date=date
        self.price=price
        self.place=place
        with open('./user_info.txt','r') as f:
            self.uid=f.readline().strip('\n').strip('\r\n').strip()
            self.upw=f.readline().strip('\n').strip('\r\n').strip()
        
    def login(self):
       self.driver.get(login_url)
#       print("###请先手动登录###")
#       while self.driver.title=='中文登录':
#           sleep(1)
       print('###开始登录###')
       self.driver.switch_to_frame('alibaba-login-box')
       self.driver.find_element_by_id('fm-login-id').send_keys(self.uid)
       self.driver.find_element_by_id('fm-login-password').send_keys(self.upw)
       self.driver.find_element_by_tag_name("button").click()
       ActionChains(self.driver).click_and_hold(self.driver.find_element_by_id('nc_1_n1z')).perform()
       ActionChains(self.driver).move_by_offset(xoffset=250, yoffset=0).perform()
       for i in range(2):
           ActionChains(self.driver).move_by_offset(xoffset=10, yoffset=0).perform()
           sleep(0.1)
       sleep(0.5)
       ActionChains(self.driver).release().perform()
       self.driver.find_element_by_tag_name("button").click()
       print("###登录成功###")
       self.driver.switch_to_default_content()
     
    def enter_concert(self):
        print('###打开浏览器，进入大麦网###')
        self.driver=webdriver.Firefox()#默认火狐浏览器
        self.driver.maximize_window()
        self.login()
        sleep(5)
        self.driver.find_elements_by_xpath('/html/body/div[1]/div/div[4]/input')[0].send_keys(self.name)
        self.driver.find_elements_by_xpath('/html/body/div[1]/div/div[4]/div[1]')[0].click()
        kinds=self.driver.find_element_by_id('category_filter_id').find_elements_by_tag_name('li')
        for k in kinds:
            if k.text=='演唱会':
                k.click()
                break
        lists=self.driver.find_elements_by_id('content_list')[0].find_elements_by_tag_name('li')
        titles=[]
        links=[]
#        root = Tk()
#        root.title("选择演唱会") 
#        v = IntVar()
#        v.set(1)
        self.choose_result=0
#        def selection():
#            self.choose_result=v.get()
#            root.destroy()
        for li in lists:
            word_link=li.find_element_by_tag_name('h3')
            titles.append(word_link.text)
            temp_s=word_link.get_attribute('innerHTML').find('href')+6
            temp_e=word_link.get_attribute('innerHTML').find('target')-2
            links.append(word_link.get_attribute('innerHTML')[temp_s:temp_e])
            if li.find_element_by_tag_name('h3').text.find(self.place)!=-1:
                self.choose_result=len(titles)
                break
#            b = Radiobutton(root,text = titles[-1],variable = v,value = len(titles),command=selection)
#            b.pack(anchor = W)
#        root.mainloop()
#        while self.choose_result==0:
#            sleep(1)
        self.url="https:"+links[self.choose_result-1]
        self.driver.get(self.url)
        print("###选择演唱会###")
    
    def choose_ticket(self):
        self.num=1
        time_start=time.time() 
        while self.driver.title.find('订单结算')==-1:
            if self.num!=1:
                self.driver.get(self.url)
            datelist=self.driver.find_elements_by_id("performList")[0].find_elements_by_tag_name('li')
            for i,j in enumerate(datelist):
                if i+1 in self.date and i!=0:
                    j.click()
            sleep(1)
            pricelist=self.driver.find_elements_by_id("priceList")[0].find_elements_by_tag_name('li')
            for i,j in enumerate(pricelist):
                if i+1 in self.price:
                    j.click()
            sleep(1)
            print("###选择演唱会时间与票价###")
        
            try:
                try:
                    for i in self.driver.find_elements_by_link_text("立即预定"):
                        if i.tag_name=='a':
                            i.click()
                except:
                    for i in self.driver.find_elements_by_link_text("立即购买"):
                        if i.tag_name=='div':
                            i.click()
            except:
                for i in self.driver.find_elements_by_link_text("选座购买"):
                        if i.tag_name=='div':
                            i.click() 
            self.num+=1
        time_end=time.time()
        print("###经过%d轮奋斗，共耗时%f秒，抢票成功！请确认订单信息###"%(self.num-1,round(time_end-time_start,3)))
                        
    def finish(self):
        self.driver.quit()
                

if __name__ == '__main__':
    con=Concert('范玮琪',[1],[1],'上海')
    con.enter_concert()
    con.choose_ticket()
    con.finish()