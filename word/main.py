import os
from selenium import webdriver
from os import path
import chnSegment
import plotWordcloud

driver = "D:/download/FORCLASS/conda/1/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = driver

# 设置为开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--headless')
browser = webdriver.Chrome(driver, options=options)
browser.maximize_window()

url=['https://mp.weixin.qq.com/s?src=11&timestamp=1621936802&ver=3090&signature=dKPZ*bAqFPEQ4AqGqWEuVcm3Q96c9otu9ZjwSs2QS7ZNSqCsTOd9Zyi2tjJgM8a4Ez-co*Ysm8jTgn3gspo5GArQaPX4skXBOQLNcEQuPAWPaD31DGZvp5YoE4DkQcUV&new=1']

f=open('./doc/word.txt',encoding="utf-8",mode='w+')
for i in url:
    browser.get(i)
    p=browser.find_element_by_id('activity-detail')
    f.write(p.text)


browser.quit()
f.close()

d = path.dirname(__file__)
text = open(path.join(d, './doc/word.txt'), encoding="utf-8", errors='ignore').read()
print(text)
# 若是中文文本，则先进行分词操作
text = chnSegment.word_segment(text)

# 生成词云
plotWordcloud.generate_wordcloud(text)
