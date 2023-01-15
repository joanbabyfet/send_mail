import logging
import time

# 日志文件
log_file = 'url_' + time.strftime("%Y%m%d", time.localtime()) + '.log'

# 写入日志
def logger(data):
    logging.basicConfig(filename = log_file, encoding = 'utf-8', level = logging.DEBUG, 
        format = '[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(data) # 根据日期生成日志

if __name__ == '__main__': # 测试运行用
    pass