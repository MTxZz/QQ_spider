#获得好友列表
import re
import time


class fri_list():
    def __init__(self,usr,session,g_tk,qzonetoken):
        self.usr = usr
        self.session = session
        self.g_tk = g_tk
        self.qzonetoken = qzonetoken
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


    def get_friend_list(self):
        # 获取好友QQ的网址,同样可以在很多与qq好友有关的网页上获取
        url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?' \
                     'uin=' + self.usr + '&do=1&fupdate=1&clean=1&g_tk=' + str(self.g_tk) + '&qzonetoken=' + self.qzonetoken

        friendIdpat = '"uin":(.*?),'
        friendNamepat = '"name":(.*?),'
        resp = self.session.get(url_friend)
        friendIdlist = re.compile(friendIdpat).findall(resp.text)
        friendNameList = re.compile(friendNamepat).findall(resp.text)
        n = len(friendIdlist)
        friend = {}
        for i in range(0,n):
            Id = friendIdlist[i]
            name = friendNameList[i]
            #db.QQ_zone.insert({'QQ号':Id,'昵称':name})
            #print('QQ号:'+Id+'   昵称:' + name)
            friend[Id] = name

        time.sleep(3)
        return friend
