import time
import pymysql
from urllib import parse
from lxml import etree
from pprint import pprint
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import requests     # 导入顺序，否则会报错
from getAccount import public_search_api

# 列表转字符串
def get_list_content(content: list):
    if content:
        content_str = str()
        for a_str in content:
            content_str += a_str
        return content_str
    else:
        return None

# 处理时间戳，获得文章推送具体时间，精确到秒 
def process_timestamp(content: int):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content))

# 文章信息
def process_html_str(html_str: str):
    html_str = etree.HTML(html_str)
    li_list = html_str.xpath('//ul[contains(@class,"news-list")]/li')
    article_list = list()
    for li in li_list:
        article = dict()
        # 筛选爬虫结果
        account = li.xpath('.//a[contains(@class,"account")]/text()')
        article['account'] = get_list_content(account)
        if article['account'] == public_info['public_name']:
            # 文章标题
            title = li.xpath('.//div[contains(@class,"txt-box")]/h3/a//text()')
            article['title'] = title[0] if title else None
            # 文章链接
            url = li.xpath('.//div[contains(@class,"txt-box")]/h3/a/@href')
            article['url'] = "https://weixin.sogou.com" + url[0] if url else None
            # 文章首图
            images = li.xpath('.//div[contains(@class,"img-box")]//img/@src')
            article['images'] = ['https:' + i for i in images] if images else None
            # 文章摘要
            abstract = li.xpath('.//p[contains(@class,"txt-info")]/text()')
            article['abstract'] = get_list_content(abstract)
            # 文章推送时间，10位时间戳
            timestamp = li.xpath('.//div[@class="s-p"]/@t')
            article['publish_date'] = process_timestamp(int(timestamp[0])) if timestamp else None
            article_list.append(article)
        else:
            continue
    return article_list 

# 解析目标地址 
def resolve_url(public_name: str):
    public_name = parse.quote(public_name)
    base_url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_=&page={}"
    # 未登录时只能获取10页结果，即当前公众号关键字的100篇文章
    url_list = [base_url.format(public_name, i) for i in range(1, 11)]
    return url_list 
 
def process_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    }
    try:
        response = requests.get(url=url, headers=headers)
        # 响应返回的数据
        if response.ok:
            article_s = process_html_str(response.text)
            return article_s
    except Exception:
        pass 
 
def public_article(public_name: str):
    url_list = resolve_url(public_name)
    # 进程池中创建三个进程
    pool = Pool(3)
    # 遍历url列表，获取文章信息
    article_list = pool.map(process_request, url_list)
    a = list()
    for a_ in article_list:
        for a__ in a_:
            a.append(a__)
    # 本次爬取到的文章数量
    print (len(a))
    return a 

# 保存公众号文章信息到数据库
def __save__(data_list):
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    account = public_info['public_name']
    # 一号一表
    cursor.execute('''CREATE TABLE IF NOT EXISTS {pName} 
                (account        VARCHAR(255)    NOT NULL,
                 title          VARCHAR(255)    NOT NULL, 
                 url            VARCHAR(2083)    NOT NULL, 
                 images         VARCHAR(255)    NOT NULL,
                 abstract       VARCHAR(255),
                 publish_date   VARCHAR(255)    NOT NULL,
                 PRIMARY KEY (title));'''.format(pName=account))
    print("初始化成功")
    for data in data_list:
        title = data['title']
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        cursor.execute('''SELECT * FROM {pName} WHERE title = \"{title}\";'''.format(pName=account, title=title))
        Article = cursor.fetchone()
        # 防止重复存取
        if Article == None:
            try:
                sql = '''INSERT INTO {pName} ({keys}) VALUES ({values});'''.format(pName=account, keys=keys, values=values)
                cursor.execute(sql, tuple(data.values()))
                db.commit()
                print('Successful')
            except Exception as e:
                print(e)
                db.rollback()
    # 插入数据和关闭数据库连接的嵌套关系
    db.close() 

if __name__ == "__main__":
    public_name = input("请输入你要查找的公众号：")
    public_info = public_search_api(public_name)
    print("公众号信息：")
    pprint(public_info)
    num = input("是否查询该作者的文章：1>是 2>否 :")
    if num == "1":
        article_list = public_article(public_name)
        __save__(article_list)
        pprint(article_list)
    else:
        print("欢迎再次使用")