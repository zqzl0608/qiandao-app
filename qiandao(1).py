import ddddocr
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.by import By
import schedule

ocr = ddddocr.DdddOcr()
Account=['zl1110','zl1111','zl1112','zl1113','zl1114','zl1115','zl1116','zl1117','zl1118','zl1119']

def captchs():
    captcha_image = driver.find_element(By.ID,'verifyCode')
    driver.switch_to.window(driver.window_handles[0])
    driver.set_window_size(929, 883)  # 设置窗口大小为929*883像素
    location = captcha_image.location
    size = captcha_image.size
    driver.save_screenshot('screenshot.png')
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = Image.open('screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('captcha.png')
    image = open("captcha.png", "rb").read()
    captcha = ocr.classification(image)
    print(captcha)
    time.sleep(5)
    captcha_input = driver.find_element(By.NAME,'captcha')
    captcha_input.clear()
    time.sleep(1)
    captcha_input.send_keys(captcha)
    receive()

def min(account):
    username_input = driver.find_element(By.NAME,'account')
    username_input.clear()
    time.sleep(1)
    username_input.send_keys(account)
    driver.find_element(By.ID,'getRoleList').click()
    time.sleep(5)
    usernames=driver.find_element(By.ID,'roles')
    Select(usernames).select_by_index(1)
    time.sleep(5)
    captchs()

def receive():
    submit_button = driver.find_element(By.ID,'SubmitBtn')
    submit_button.click()
    time.sleep(5)
    captch = driver.find_element(By.CLASS_NAME,'modal-body').text
    if captch=='领取成功！':
        print(captch)
        button = driver.find_element(By.CLASS_NAME,'btn-primary')
        button.click()
    elif '领取次数已达上限' in captch:
            print(captch)
            button = driver.find_element(By.CLASS_NAME,'btn-primary')
            button.click()
    else:
        print(captch)
        button=driver.find_element(By.CLASS_NAME,'btn-primary')
        button.click()
        time.sleep(5)
        driver.find_element(By.ID,'verifyCode').click()
        time.sleep(3)
        captchs()

def a():
    for account in Account:
        print(account)
        min(account)

if __name__ == '__main__':
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')  # 禁用沙盒模式
    chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
    
    # 初始化Chrome驱动
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get('http://zssgs.yxgmaet.com/index/gift?p=qd')
        time.sleep(3)
        server_input = driver.find_element(By.NAME,'server')
        options_list = Select(server_input).options
        Select(server_input).select_by_value("230004")
        a()
    finally:
        driver.quit()
