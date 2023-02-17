import urllib.request
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

keyword = input("검색어: ")

driver = webdriver.Chrome()
driver.get('https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + quote_plus(keyword))
driver.implicitly_wait(3)

test = driver.find_elements(By.CLASS_NAME, "_image._listImage")
images_url = []
for i in test:
    if i.get_attribute('src')!=None:
        images_url.append(i.get_attribute('src'))
    else:
        images_url.append(i.get_attribute('data-src'))
driver.close()

print(images_url)

cnt = 0
for i in range(0, len(images_url)):
    try:
        urllib.request.urlretrieve(images_url[i], "./crawled_img/"+str(cnt)+'.jpg')
    except:
        continue
    cnt+=1
    sleep(0.1)

