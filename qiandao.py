import ddddocr
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# 先导入修补模块
import pillow_patch
from PIL import Image
from selenium.webdriver.common.by import By
import schedule
import os

# 直接使用已知的Chrome路径
CHROME_PATH = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Bin\Google Chrome.exe"

# 初始化OCR
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
    # 保存前检查ddddocr是否需要特定尺寸的图片
    im.save('captcha.png')
    
    # 直接使用二进制方式打开图片
    with open("captcha.png", "rb") as f:
        image = f.read()
    
    # 识别验证码
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
    if not os.path.exists(CHROME_PATH):
        print(f"错误：在指定路径找不到Chrome浏览器: {CHROME_PATH}")
        exit(1)
    
    print(f"使用Chrome浏览器路径: {CHROME_PATH}")
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 启用无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 指定Chrome浏览器路径
    chrome_options.binary_location = CHROME_PATH
    
    # 使用指定的ChromeDriver路径
    service = Service(executable_path=r"D:\新建文件夹\chromedriver-win64\chromedriver.exe")
    
    try:
        # 初始化Chrome驱动
        print("正在启动Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome启动成功")
        
        driver.get('https://sgs.zce8.com/index/cdk')
        time.sleep(3)
        server_input = driver.find_element(By.NAME,'server')
        options_list = Select(server_input).options
        Select(server_input).select_by_value("3")
        cdk_input = driver.find_element(By.NAME,'cdk')
        cdk_input.send_keys('sgs2025')
        a()
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

