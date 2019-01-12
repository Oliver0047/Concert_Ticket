# Concert_Ticket
大麦网演唱会抢票程序
* Python3.6
* Selenium

 ```Python
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
 ```
