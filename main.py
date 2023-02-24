import urllib.request
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from time import sleep

urls = []


def get_image_urls(driver, wait=.1, retry=3):
    def check_loaded(img):
        return False if img.get_attribute('src').endswith('type=a340') else True

    # body = driver.find_element_by_tag_name('body')
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.HOME)
    imgs = driver.find_elements(By.XPATH, '//img[@class="_image _listImage"]')
    for n, img in enumerate(imgs):
        if n == 0:
            img.click()
        count = retry
        origin_img = driver.find_element(By.XPATH, '//div[@class="image _imageBox"]//img')
        while count and not check_loaded(origin_img):
            sleep(wait)
            count -= 1

        if check_loaded(origin_img):
            urls.append(origin_img.get_attribute('src'))

        body.send_keys(Keys.RIGHT)
    print(f'{len(urls)}/{len(imgs)} images are loaded')
    return urls


def scroll_page():
    initial_height = driver.execute_script("return document.body.scrollHeight")

    first_scrollHeight = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        first_scrollHeight += driver.execute_script("return document.body.scrollHeight")
        sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == initial_height:
            break
        initial_height = new_height

    sleep(1.5)


def save_img():
    cnt = 0
    for i in range(0, len(urls)):
        try:
            urllib.request.urlretrieve(urls[i], "./crawled_img/" + str(cnt) + '.jpg')
        except:
            continue
        cnt += 1
        sleep(1)


keyword = input("검색어: ")
# cnt = input("페이지 수: ")

driver = webdriver.Chrome()
driver.get('https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + quote_plus(keyword))
driver.implicitly_wait(3)

scroll_page()
get_image_urls(driver, wait=.1, retry=3)
save_img()
