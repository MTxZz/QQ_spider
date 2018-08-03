#获取爬取链接需要的东西
import requests

class Cookie():
    def __init__(self,cookie):
        self.cookie = cookie
        self.headers = {
            'authority': 'user.qzone.qq.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        }
        self.url = 'https://user.qzone.qq.com/'


    def get_g_tk(self):
        hashes = 5381
        for c in self.cookie['p_skey']:
            hashes += (hashes << 5) + ord(c)#return a unicode
        return hashes & 0X7fffffff

    def get_session(self):
        session = requests.session()
        c = requests.utils.cookiejar_from_dict(self.cookie,cookiejar = None,overwrite = True)
        session.headers = self.headers
        session.cookies.update(c)
        return session
