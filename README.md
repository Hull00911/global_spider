# 环球时报标题爬取与预测
## 使用教程
1. [点击这里下载][1]下载chrome浏览器
2. 查看chrome浏览器的版本号，[点击这里下载][2]对应版本号的chromedriver驱动
3. pip安装下列包
- [x] pip install selenium
- [x] pip install tensorflow
4.将安装包解压至桌面
5. 在main中填写chromedriver的绝对路径
6. 在main中填写爬取网站的网址

```python
	#改成你的chromedriver的完整路径地址
    chromedriver_path = "/Users/bird/Desktop/chromedriver.exe" 
    #改成目标网址
    weibo_username = "改成目标网址"
```

[1]:https://www.google.com/chrome/
[2]:http://chromedriver.storage.googleapis.com/index.html
