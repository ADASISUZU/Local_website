# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 20:50:00 2020

@author: AKadam
"""

from selenium import webdriver

chrome_path = r"C:\Users\akadam\Desktop\chromedriver.exe"
driver  =  webdriver.Chrome(chrome_path)
driver.get("https://automotivedigest.com/events/")
posts = driver.find_elements_by_class_name("event_name")
for post in posts:
    print(post.text)