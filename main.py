import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import os
import configparser
import pandas as pd
import logging
import time

# 配置文件
config_file = 'config.ini' 
# 日志文件
log_file = 'mail_' + time.strftime("%Y%m%d", time.localtime()) + '.log'

# 发送邮件
def send_mail(item):
    # 这里要转字符串, 否则文本为数字会报错, 空值会返回nan也要处理
    to      = '' if pd.isnull(item['email']) else str(item['email']) # 收件人邮箱
    to_name = '' if pd.isnull(item['name']) else str(item['name'])   # 收件人名称
    subject = '' if pd.isnull(item['subject']) else str(item['subject']) # 主旨
    content = '' if pd.isnull(item['content']) else str(item['content']) # 内容
    
    try:
        conf = configparser.ConfigParser()
        conf.read(config_file, encoding='utf-8') # 这里要加utf-8, 否则会报错, 默认gbk
        config_section      = 'mail_config'
        mail_host           = conf.get(config_section, 'mail_host')
        mail_port           = conf.get(config_section, 'mail_port')
        mail_username       = conf.get(config_section, 'mail_username')
        mail_password       = conf.get(config_section, 'mail_password')
        mail_from           = conf.get(config_section, 'mail_from')
        mail_from_name      = conf.get(config_section, 'mail_from_name')
        subject             = item['subject'] 
        message             = MIMEText(content , 'plain', 'utf-8') # 文本内容/文本格式/文本编码
        message['From']     = formataddr([mail_from_name, mail_from], 'utf-8') # 发送者
        message['To']       = formataddr([to_name, to], 'utf-8')   # 收件人, formataddr列表转字符串
        message['Subject']  = Header(subject, 'utf-8')

        smtp = smtplib.SMTP_SSL(mail_host, mail_port) # gmail安全性用ssl
        smtp.login(mail_username, mail_password)
        if to != '':
            smtp.sendmail(mail_from, to, message.as_string()) # 发送邮件
            msg = '%s 发送成功' % message['To']
        else:
            msg = '%s 发送失败' % message['To']

        smtp.quit() # 关闭连接, 结束smtp对象
        logger(msg) # 写入日志
        print(msg)
    except smtplib.SMTPException as e:
        msg = '%s 发送失败' % e
        logger(msg) # 写入日志
        print(msg)

# 写入日志
def logger(data):
    logging.basicConfig(filename = log_file, encoding = 'utf-8', level = logging.DEBUG, 
        format = '[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(data) # 根据日期生成日志

def main():
    if not os.path.exists(os.path.join(os.getcwd(), config_file)): # 检测配置文件是否存在
        print('%s 配置文件不存在' % config_file)
    else:
        df = pd.read_csv('list.csv', encoding='utf-8')
        df.apply(send_mail, axis=1) # apply添加send_mail函数, 且数据逐行加入

if __name__ == '__main__': # 主入口
    main()