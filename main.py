import random,re,time,os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from keras import models,regularizers,layers
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np

class global_spider():
    def __init__(self,target_url,chromedriver_path):
        self.url=target_url
        f = open('dict.txt','r+',encoding='gbk')
        self.dict=eval(f.read())
        self.browser = webdriver.Chrome(chromedriver_path)
        self.wait = WebDriverWait(self.browser,10)

    # 爬取环球时报指定标题用于测试
    def crawl(self,number):

        # 爬取标题

        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.browser.execute_script(js)
        time.sleep(1)
        try:
            str = self.browser.find_element_by_xpath(f'//ul[@id="recommend"]/li[{number + 2}]//h4').text
        except:
            return -1
        print(str)
        return str

    # 对爬取的字符串进行处理
    def process(self,str):

        # 对字符串正则化仅保留汉字
        re_str = ''.join(re.findall('[\u4e00-\u9fa5]', str))

        # 随机删除一个字符
        list = [str]
        for s in range(9):
            num = random.randint(0, len(str) - 1)
            new_str = str[0:num] + str[num + 1:len(str)]
            list.append(new_str)

        # 汉字转换为数字
        list_digital = []
        for str1 in list:
            list_temp = [[]]
            for s in str1:
                list_temp[0].append(self.dict.get(s, 0))
            list_digital.append(list_temp)
        return list_digital

    # 导入模型预测结果
    def predict(self,pre,dimension=4000):

        # 转换为numpy矩阵
        index = np.zeros((len(pre), dimension))
        for s, i in enumerate(pre):
            for m in i:
                index[s, m] = 1

        # 导入模型设定层
        model = models.Sequential()
        model.add(layers.Dense(64, kernel_regularizer=regularizers.l2(0.001), activation='relu', input_shape=(4000,)))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(64, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(6, activation='softmax'))
        model.load_weights('weights.best.hdf5')

        # 预测结果
        predict = model.predict(index)
        return np.argmax(predict[0]) + 1

    # 连接到指定网址
    def open(self):
        try:
            self.browser.get(self.url)
        except:
            print("当前网络状态不佳，重连后再试")
            exit()
        time.sleep(1)

    # 关闭浏览器
    def close(self):
        self.browser.close()




if __name__ == "__main__":
    chromedriver_path="改成驱动安装地址"
    '''
    财经: https://finance.huanqiu.com
    健康: https://health.huanqiu.com
    军事: https://mil.huanqiu.com
    科技: https://tech.huanqiu.com
    汽车: https://auto.huanqiu.com
    社会: https://society.huanqiu.com
    '''
    target_url="改成目标网址"

    a=global_spider(target_url,chromedriver_path)
    a.open()
    for i in range(10):
        title = a.crawl(i)
        if title == -1:
            continue
        title_digital = a.process(title)
        count = [0, 0, 0, 0, 0, 0]
        for s in title_digital:
            result = a.predict(s)
            count[result-1] += 1
        max = 0
        po = 0
        for s in range(6):
            if max < count[s]:
                max = count[s]
                po = s
        if po == 0:
            print("财经", end='')
        if po == 1:
            print("健康", end='')
        if po == 2:
            print("军事", end='')
        if po == 3:
            print('科技', end='')
        if po == 4:
            print('汽车', end='')
        if po == 5:
            print('社会', end='')
        print(f" 概率为{max * 10}%")
    a.close()