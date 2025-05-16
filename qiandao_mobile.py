import requests
import time
import logging
from datetime import datetime
import json
import os

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

def get_captcha(session):
    try:
        # 获取验证码图片
        response = session.get('https://sgs.zce8.com/index/captcha')
        if response.status_code == 200:
            # 保存验证码图片
            with open('captcha.png', 'wb') as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        logging.error(f"获取验证码失败: {str(e)}")
        return False

def process_account(session, account):
    try:
        logging.info(f"处理账号: {account}")
        
        # 获取角色列表
        data = {
            'account': account,
            'server': '3'
        }
        response = session.post('https://sgs.zce8.com/index/getRoleList', data=data)
        if response.status_code != 200:
            logging.error(f"获取角色列表失败: {response.text}")
            return
        
        # 选择第一个角色
        roles = response.json().get('data', [])
        if not roles:
            logging.error(f"账号 {account} 没有可用角色")
            return
        
        role_id = roles[0].get('id')
        
        # 获取验证码
        if not get_captcha(session):
            return
        
        # 这里需要手动输入验证码
        captcha = input(f"请查看captcha.png图片并输入验证码: ")
        
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
            logging.info(f"领取结果: {result.get('msg', '未知结果')}")
        else:
            logging.error(f"提交失败: {response.text}")
            
    except Exception as e:
        logging.error(f"账号 {account} 处理出错: {str(e)}")

def run_task():
    logging.info("开始执行签到任务")
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        })
        
        for account in Account:
            try:
                process_account(session, account)
            except Exception as e:
                logging.error(f"账号 {account} 处理失败: {str(e)}")
                continue
            time.sleep(5)  # 账号之间等待5秒
            
    except Exception as e:
        logging.error(f"任务执行出错: {str(e)}")

def wait_until_next_run():
    now = datetime.now()
    next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
    if now >= next_run:
        next_run = next_run.replace(day=next_run.day + 1)
    wait_seconds = (next_run - now).total_seconds()
    logging.info(f"等待 {wait_seconds/3600:.1f} 小时后执行下一次任务")
    time.sleep(wait_seconds)

if __name__ == '__main__':
    while True:
        run_task()
        wait_until_next_run() 