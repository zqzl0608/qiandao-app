from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import requests
import time
import logging
from datetime import datetime
import json
import os
from threading import Thread
import ddddocr
from PIL import Image as PILImage
import io

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qiandao.log'),
        logging.StreamHandler()
    ]
)

Account=['zl1110','zl1111','zl1112','zl1113','zl1114','zl1115','zl1116','zl1117','zl1118','zl1119']

class QiandaoApp(App):
    def build(self):
        # 设置窗口大小
        Window.size = (400, 600)
        
        # 创建主布局
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 状态标签
        self.status_label = Label(text='准备就绪', size_hint_y=None, height=50)
        self.layout.add_widget(self.status_label)
        
        # 验证码图片显示
        self.captcha_image = Image(source='captcha.png', size_hint_y=None, height=100)
        self.layout.add_widget(self.captcha_image)
        
        # 开始按钮
        self.start_button = Button(text='开始运行', size_hint_y=None, height=50)
        self.start_button.bind(on_press=self.start_task)
        self.layout.add_widget(self.start_button)
        
        # 日志显示区域
        self.log_label = Label(text='', size_hint_y=1)
        self.layout.add_widget(self.log_label)
        
        # 初始化OCR
        self.ocr = ddddocr.DdddOcr()
        
        return self.layout
    
    def update_status(self, text):
        self.status_label.text = text
        self.log_label.text = text + '\n' + self.log_label.text
    
    def get_captcha(self, session):
        try:
            response = session.get('https://sgs.zce8.com/index/captcha')
            if response.status_code == 200:
                # 保存验证码图片
                with open('captcha.png', 'wb') as f:
                    f.write(response.content)
                self.captcha_image.reload()
                
                # 识别验证码
                captcha = self.ocr.classification(response.content)
                self.update_status(f"验证码识别结果: {captcha}")
                return captcha
            return None
        except Exception as e:
            self.update_status(f"获取验证码失败: {str(e)}")
            return None
    
    def process_account(self, session, account):
        try:
            self.update_status(f"处理账号: {account}")
            
            # 获取角色列表
            data = {
                'account': account,
                'server': '3'
            }
            response = session.post('https://sgs.zce8.com/index/getRoleList', data=data)
            if response.status_code != 200:
                self.update_status(f"获取角色列表失败: {response.text}")
                return
            
            # 选择第一个角色
            roles = response.json().get('data', [])
            if not roles:
                self.update_status(f"账号 {account} 没有可用角色")
                return
            
            role_id = roles[0].get('id')
            
            # 获取并识别验证码
            captcha = self.get_captcha(session)
            if not captcha:
                return
            
            # 提交领取请求
            data = {
                'account': account,
                'server': '3',
                'role_id': role_id,
                'cdk': 'sgs2025',
                'captcha': captcha
            }
            response = session.post('https://sgs.zce8.com/index/submit', data=data)
            
            if response.status_code == 200:
                result = response.json()
                self.update_status(f"领取结果: {result.get('msg', '未知结果')}")
                
                # 如果验证码错误，重试
                if '验证码错误' in result.get('msg', ''):
                    self.update_status("验证码错误，重试中...")
                    time.sleep(2)
                    return self.process_account(session, account)
            else:
                self.update_status(f"提交失败: {response.text}")
                
        except Exception as e:
            self.update_status(f"账号 {account} 处理出错: {str(e)}")
    
    def run_task(self):
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
            })
            
            for account in Account:
                try:
                    self.process_account(session, account)
                except Exception as e:
                    self.update_status(f"账号 {account} 处理失败: {str(e)}")
                    continue
                time.sleep(5)
                
        except Exception as e:
            self.update_status(f"任务执行出错: {str(e)}")
    
    def start_task(self, instance):
        self.start_button.disabled = True
        Thread(target=self.run_task).start()
        self.start_button.disabled = False

if __name__ == '__main__':
    QiandaoApp().run() 