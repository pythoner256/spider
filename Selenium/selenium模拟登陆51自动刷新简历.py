
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

url = 'https://login.51job.com/login.php?lang=c'
browser = webdriver.Chrome()
browser.get(url)
sleep(2)

username = browser.find_element_by_id('loginname')
username.send_keys('自己的账号')
password = browser.find_element_by_id('password')
password.send_keys('密码')
browser.find_element_by_id('login_btn').click()

browser.execute_script("setInterval (re, 6000);function re(){refresh_resume(378963217,'c','//i.51job.com/resume');};")

