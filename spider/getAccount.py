import requests
import pymysql
from urllib import parse
from lxml import etree
from pprint import pprint

# 列表转字符串 
def get_list_content(content: list):
    if content:
        content_str = str()
        for a_str in content:
            content_str += a_str
        return content_str
    else:
        return None

# 公众号信息 
def process_html_str(html_str):
    html_str = etree.HTML(html_str)
    li_list = html_str.xpath('//ul[contains(@class, "news-list2")]/li')
    public_info = list()
    for li in li_list:
        item = dict()
        # 公众号名称
        public_name = li.xpath('.//p[contains(@class, "tit")]/a//text()')
        item["public_name"] = get_list_content(public_name)
        # 微信号
        wechat_id = li.xpath('.//p[contains(@class, "info")]/label/text()')
        item["wechat_id"] = wechat_id[0] if wechat_id else None
        # 头像
        publish_image = li.xpath('.//div[contains(@class,"ew-pop")]//span[@class="pop"]/img[2]/@src')
        item["public_image"] = "https:" + publish_image[0] if publish_image else None
        # 微信认证
        authentication = li.xpath('.//i[@class="identify"]/../text()')
        item['authentication'] = authentication[1] if authentication else None
        # 简介
        introduction = li.xpath('.//dl[1]/dd//text()')
        item["introduction"] = get_list_content(introduction)
        public_info.append(item)
    return public_info

# 关键词查询 
def public_search(public_name: str):
    public_name = parse.quote(public_name)
    base_url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_="
    # 目标地址
    url = base_url.format(public_name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    }
    # 响应返回的数据
    response = requests.get(url=url, headers=headers)
    if response.ok:
        return process_html_str(response.text)

# 精准查询 
def public_search_api(public_name):
    public_info = public_search(public_name)
    for info in public_info:
        pprint("No{}:{}".format(public_info.index(info), info["public_name"]))
    num = int(input("请选择要查询的公众号:"))
    return public_info[num]

# 保存公众号信息到数据库
def __save__(data):
    # 修改数据库连接配置
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    wID = data['wechat_id']
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    cursor.execute('''SELECT * FROM Accounts WHERE wechat_id = \"{wechatid}\";'''.format(wechatid=wID))
    AccountInfo = cursor.fetchone()
    # 防止重复存取
    if AccountInfo == None:
        try:
            sql = '''INSERT INTO Accounts ({keys}) VALUES ({values});'''.format(keys=keys, values=values)
            cursor.execute(sql, tuple(data.values()))
            db.commit()
            print('Successful')
        except Exception as e:
            print(e)
            db.rollback()
        db.close()
    else:
        pprint("Existed record.")

def keyword_search_api(keyword:str):
    
    account_infos = public_search(keyword)

    # store accounts
    for info in account_infos:
        __save__(info)

    return account_infos
 
def run():
    # 获取公众号名称
    public_name = input("请输入你要查找的公众号：")
    public_info = public_search_api(public_name)
    # 存储爬取结果
    __save__(public_info)
    pprint(public_info)
 
if __name__ == "__main__":
    run()