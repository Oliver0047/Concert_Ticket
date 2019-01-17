# -*- coding: utf-8 -*-
#autor:Oliver0047
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep
import re
from tkinter import *
import time
import pickle
import os

damai_url="https://www.damai.cn/"
login_url="https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
class Concert(object):
    def __init__(self,name,date,price,place,real_name,method=1):
        self.name=name#歌星
        self.date=date#日期序号优先级，比如，如果第二个时间可行，就选第二个，不然就选其他,最终只选一个
        self.price=price#票价序号优先级,道理同上
        self.place=place#地点
        self.status=0#状态,表示如今进行到何种程度
        self.login_method=method#{0:模拟登录,1:Cookie登录}自行选择登录方式
        self.real_name=real_name#实名者序号
        with open('./user_info.txt','r') as f:#读入用户名与密码和昵称
            self.uid=f.readline().strip('\n').strip('\r\n').strip()
            self.upw=f.readline().strip('\n').strip('\r\n').strip()
            self.usr_name=f.readline().strip('\n').strip('\r\n').strip()
            
    def get_cookie(self):
       self.driver.get(damai_url)
       print("###请点击登录###")
       while self.driver.title.find('大麦网-全球演出赛事官方购票平台')!=-1:
           sleep(1)
       print("###请扫码登录###")
       while self.driver.title=='中文登录':
           sleep(1)
       print("###扫码成功###")
       pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb")) 
       print("###Cookie保存成功###")
    
    def set_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))#载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain':'.damai.cn',#必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)
            
    def login(self):
        if self.login_method==0:
            self.driver.get(login_url)#载入登录界面
            print('###开始登录###')
            sleep(1)
            self.driver.switch_to.frame('alibaba-login-box')#里面这个是iframe的id
            self.driver.find_element_by_id('fm-login-id').send_keys(self.uid)
            self.driver.find_element_by_id('fm-login-password').send_keys(self.upw)
            self.driver.find_element_by_tag_name("button").click()
            try:
                ActionChains(self.driver).click_and_hold(self.driver.find_element_by_id('nc_1_n1z')).perform()#按住滑块不动
                ActionChains(self.driver).move_by_offset(xoffset=250, yoffset=0).perform()#直接到终点，可能速度太快，会被系统判错误操作
                for i in range(2):
                    ActionChains(self.driver).move_by_offset(xoffset=10, yoffset=0).perform()#再慢慢滑两步
                    sleep(0.1)
                ActionChains(self.driver).release().perform()#松开点击
                sleep(1)#滑完了之后稍等下，让系统判断完毕
                self.driver.find_element_by_tag_name("button").click()
                self.driver.switch_to.default_content()
            except Exception as e:
                print(e)
        elif self.login_method==1:            
            if not os.path.exists('cookies.pkl'):#如果不存在cookie.pkl,就获取一下
                self.get_cookie()
            else:
                self.driver.get(damai_url)
                self.set_cookie()
     
    def enter_concert(self):
        print('###打开浏览器，进入大麦网###')
        self.driver=webdriver.Firefox()#默认火狐浏览器
        self.driver.maximize_window()
        self.login()#先登录再说
        self.driver.refresh()
        sleep(1)
        if self.driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[1]/a[2]/div').text==self.usr_name:
            self.status=1
            print("###登录成功###")
        else:
            self.status=0
            print("###登录失败###")
        if self.status==1:
            self.driver.find_elements_by_xpath('/html/body/div[2]/div/div[4]/input')[0].send_keys(self.name)#搜索栏输入歌星
            self.driver.find_elements_by_xpath('/html/body/div[2]/div/div[4]/div[1]')[0].click()#点击搜索
            kinds=self.driver.find_element_by_id('category_filter_id').find_elements_by_tag_name('li')#选择演唱会类别
            for k in kinds:
                if k.text=='演唱会':
                    k.click()
                    break
            lists=self.driver.find_elements_by_id('content_list')[0].find_elements_by_tag_name('li')#获取所有可能演唱会
            titles=[]
            links=[]
            #注释的代码表示用图形界面手动选择演唱会，可以自行体会
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
                if li.find_element_by_tag_name('h3').text.find(self.place)!=-1:#选择地点正确的演唱会
                    self.choose_result=len(titles)
                    break
    #            b = Radiobutton(root,text = titles[-1],variable = v,value = len(titles),command=selection)
    #            b.pack(anchor = W)
    #        root.mainloop()
    #        while self.choose_result==0:
    #            sleep(1)
            self.url="https:"+links[self.choose_result-1]
            self.driver.get(self.url)#载入至购买界面
            self.status=2
            print("###选择演唱会###")
    
    def choose_ticket(self):
        if self.status==2:
            self.num=1#第一次尝试
            time_start=time.time() 
            while self.driver.title.find('订单结算')==-1:#如果跳转到了订单结算界面就算这部成功了
                if self.num!=1:#如果前一次失败了，那就刷新界面重新开始
                    self.status=2
                    self.driver.get(self.url)
                datelist=self.driver.find_element_by_id("performList").find_elements_by_tag_name('li')
                for i in self.date:#根据优先级选择一个可行日期
                    j=datelist[i-1].get_attribute('class')
                    if j=='itm':
                        datelist[i-1].click()
                        break
                    elif j=='itm itm-sel':
                        break
                    elif j=='itm itm-oos':
                        continue
                sleep(1)
                pricelist=self.driver.find_element_by_id("priceList").find_elements_by_tag_name('li')#根据优先级选择一个可行票价
                for i in self.price:
                    j=pricelist[i-1].get_attribute('class')
                    if j=='itm':
                        pricelist[i-1].click()
                        break
                    elif j=='itm itm-sel':
                        break
                    elif j=='itm itm-oos':
                        continue
                sleep(1.5)
                print("###选择演唱会时间与票价###")
                cart=self.driver.find_element_by_id('cartList')
                try:#各种按钮的点击
                    try:
                        cart.find_element_by_class_name('ops').find_element_by_link_text("立即预定").click()
                        self.status=3
                    except:
                        cart.find_element_by_class_name('ops').find_element_by_link_text("立即购买").click()
                        self.status=4
                except:
                    cart.find_element_by_class_name('ops').find_element_by_link_text("选座购买").click()
                    self.status=5
                self.num+=1
                sleep(0.5)
            time_end=time.time()
            print("###经过%d轮奋斗，共耗时%f秒，抢票成功！请确认订单信息###"%(self.num-1,round(time_end-time_start,3)))
    
    def check_order(self):
        if self.status in [3,4,5]:
            print('###开始确认订单###')
            print('###默认购票人信息###')  
            rn_button=self.driver.find_elements_by_xpath('/html/body/div[3]/div[3]/div[2]/div[2]/div/a')
            if len(rn_button)==1:#如果要求实名制
                print('###选择实名制信息###')
                rn_button[0].click()
                #选择实名信息
                tb=self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[12]/div')
                lb=tb.find_elements_by_tag_name('label')[self.real_name]#选择第self.real_name个实名者
                lb.find_elements_by_tag_name('td')[0].click()
                tb.find_element_by_class_name('one-btn').click()
            print('###默认选择付款方式###')
            print('###确认商品清单###')
            rn_button=self.driver.find_elements_by_xpath('/html/body/div[3]/div[3]/div[3]/div[2]/div[2]/div/div/h2/a[1]')
            if len(rn_button)==1:#如果要求实名制
                print('###选择购票人信息###')
                rn_button[0].click()
                #选择实名信息
                tb=self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[13]/div')
                lb=tb.find_elements_by_tag_name('label')[self.real_name]#选择第self.real_name个实名者
                lb.find_elements_by_tag_name('td')[0].click()
                tb.find_element_by_class_name('one-btn').click()
            print('###不选择订单优惠###')
            print('###请在付款完成后下载大麦APP进入订单详情页申请开具###')
            self.driver.find_element_by_id('orderConfirmSubmit').click()#同意以上协议并提交订单
            sleep(8)
            if self.driver.title.find('支付')!=-1:
                self.status=6
                print('###成功提交订单,请手动支付###')
            else:
                print('###提交订单失败,请查看问题###')
                        
    def finish(self):
        self.driver.quit()
                

if __name__ == '__main__':
    try:
        con=Concert('范玮琪',[1],[1],'上海',1)#具体如何填写请查看类中的初始化函数
        con.enter_concert()
        con.choose_ticket()
        con.check_order()
    except Exception as e:
        print(e)
        con.finish()
