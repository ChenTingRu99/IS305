import requests
from urllib import parse
from lxml import etree
from pprint import pprint
 
def process_list_content(content: list):
    if content:
        content_str = str()
        for a_str in content:
            content_str += a_str
        return content_str
    else:
        return None
 
def process_html_str(html_str):
    html_str = etree.HTML(html_str)
    li_list = html_str.xpath('//ul[contains(@class, "news-list2")]/li')
    public_info = list()
    for li in li_list:
        item = dict()
        public_name = li.xpath('.//p[contains(@class, "tit")]/a//text()')
        item["public_name"] = process_list_content(public_name)
        wechat_id = li.xpath('.//p[contains(@class, "info")]/label/text()')
        item["wechat_id"] = wechat_id[0] if wechat_id else None
        publish_qrcode = li.xpath('.//div[contains(@class,"ew-pop")]//span[@class="pop"]/img[1]/@src')
        item["public_qrcode"] = publish_qrcode[0] if publish_qrcode else None
        publish_image = li.xpath('.//div[contains(@class,"ew-pop")]//span[@class="pop"]/img[2]/@src')
        item["public_image"] = "https:" + publish_image[0] if publish_image else None
        authentication = li.xpath('.//i[@class="identify"]/../text()')
        item['authentication'] = authentication[1] if authentication else None
        introduction = li.xpath('.//dl[1]/dd//text()')
        item["introduction"] = process_list_content(introduction)
        public_info.append(item)
    return public_info
 
def public_search(public_name: str):
    public_name = parse.quote(public_name)
    base_url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_="
    url = base_url.format(public_name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    }
    response = requests.get(url=url, headers=headers)
    if response.ok:
        return process_html_str(response.text)
 
def public_search_api(public_name):
    public_info = public_search(public_name)
    for info in public_info:
        pprint("No{}:{}".format(public_info.index(info), info["public_name"]))
    num = int(input("请选择要查询的公众号:"))
    return public_info[num]
 
def run():
    public_name = input("请输入你要查找的公众号：")
    public_info = public_search_api(public_name)
    pprint(public_info)
 
if __name__ == "__main__":
    run()