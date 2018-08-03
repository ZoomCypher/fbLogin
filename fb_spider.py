import requests
from user_agents import agents
import random
import datetime
import json
import pymysql
import time


# fg = 0
# starttime = datetime.datetime.now()
# while True:
#     try:
#         account = "ifengglobal"
#         access_token = "EAAAAUaZA8jlABAIJZCeT8GmFV047xm7trqodwRjCY630aB0y48n7K5SK8oowH3ddqq4hfSfZBNer271JXVpVOpU7zZCGx4IX7a1nLmuMOXM5Mqujet9ZB659v06XNSPde46vJZCrlr8J5L9sSdG50Fe43cG5RnUDyTeXKZClGZBcZB5tpOsmZBDKHwDg6YOzJqtstbJ0l5WDKngqQrbx2GAojm"

#         url = 'https://graph.facebook.com/{}/posts?&access_token={}'.format(account, access_token)

#         headers = {}
#         headers['User-Agent'] = random.choice(agents)
#         res = requests.get(url, headers=headers)
#         content = res.text

#         if "Error validating access token" in content:
#             break

#         fg += 1
#         print("次数统计:", fg)
#     except:
#         pass

# endtime = datetime.datetime.now()
# print("运行时长", (endtime - starttime), "次数", fg)

class FbSpider(object):

    def __init__(self):
        self.pageCount = 1
        self.db = pymysql.connect(
            host='119.145.230.3', 
            user='root',
            password='izhonghong@2016root123',
            db='fb_resource_center',
            port=53306
        )
        self.cursor = self.db.cursor()
    


    def refresh_mysql(self):
        try:
            self.db = pymysql.connect(
                host='119.145.230.3', 
                user='root',
                password='izhonghong@2016root123',
                db='fb_resource_center',
                port=53306
            )
            self.cursor = self.db.cursor()
        except Exception as e:
            print('refresh:', e)
            time.sleep(10)


    def getAccount(self):
        try:
            sql = 'select user_domain from user_list where crawl_tg is NULL LIMIT 1'
            self.cursor.execute(sql)
            account = self.cursor.fetchone()[0]
            now = datetime.datetime.now()
            print("%s 正在获取待爬用户: %s" % (now, account))
        except Exception as e:
            print(e)
        return account
    

    def tagAccountAsWhole(self, account):
        try:
            sql = 'update user_list set crawl_tg = 1 where user_domain = "%s"' % account
            self.cursor.execute(sql)
            self.db.commit()
            now = datetime.datetime.now()
            print("%s 用户：%s ,已完成全量爬取!" % (now, account))
        except Exception as e:
            print(e)
    

    
    def getToken(self):
        try:
            sql = 'select token from fb_access_token where valid_tg is NULL LIMIT 1'
            self.cursor.execute(sql)
            token = self.cursor.fetchone()[0]
            now = datetime.datetime.now()
            if token == None:
                print(now, "没有token,等待获取中...")
            print(now, "获取token成功，正在检查是否失效...")
        except Exception as e:
            print(e)
        
        if self.checkTokenValidity(token) == False:
            try:
                sql = 'update fb_access_token set valid_tg = 1 where token = "%s"' % token
                self.cursor.execute(sql)
                self.db.commit()
                now = datetime.datetime.now()
                print(now, "token已失效，已在数据库标记为失效, 正在切换..")
            except Exception as e:
                print(e)

            # 失效则回调
            return None
            time.sleep(5)
            
        else:
            return access_token
    

    def checkTokenValidity(self, token):
        try:
            url = "https://graph.facebook.com/DonaldTrump/posts?&access_token={}".format(token)
            headers = {}
            headers['User-Agent'] = random.choice(agents)
            res = requests.get(url, headers=headers, timeout=5)
            content = res.text
            if "Error validating access token" in content:
                return False
            return True
        except Exception as e:
            print(e)
            return False


    def fullCrawlList(self):
        pass
    

    def updateCrawlList(self):
        pass
    

    def startRequest(self, url, access_token, account):

        if '__paging_token'  not in url:
            url = 'https://graph.facebook.com/{}/posts?&access_token={}'.format(account, access_token)

        headers = {}
        headers['User-Agent'] = random.choice(agents)
        res = requests.get(url, headers=headers)
        content = res.text

        content = json.loads(content)
        data_lst = content["data"]

        print("page: %s" % self.pageCount)
        for data in data_lst:
            account_name = data["from"]["name"]
            text = data["message"]
            url = data["link"]
            time = data["updated_time"]
            zan = data["likes"]["count"]
            print(access_name, text, url, time, zan)

        if content['paging']['next']:
            self.pageCount =+ 1
            url = content['paging']['next']
            self.startCrawling(url, access_token, account)
        
        else:
            self.tagAccountAsWhole(account)

    
    def startCrawling(self, url, access_token, account):

        # 验证失败，开始切换
        if self.checkTokenValidity(token) == False:
            # token失效,切换后需要验证token是否有效
            access_token = self.getToken()
            # 有效则爬取
            if access_token != None: 
                self.startRequest(url, access_token, account)
            # 无效则过滤
            else:
                pass
        # 验证成功，开始爬取
        else:
            self.startRequest(url, access_token, account)
           

    def run():
        
        while True:
            # 开始前验证token
            access_token = self.getToken()
            if access_token != None: 
                now = datetime.datetime.now()
                account =  self.getAccount()
                print(now, "token获取成功, 开始爬取用户: %s" % account)
                # 组装首页url
                url = 'https://graph.facebook.com/{}/posts?&access_token={}'.format(account, access_token)
                self.startCrawling(url, access_token, account)
    


            
    




if __name__ == "__main__":

    fs = FbSpider()
    # fs.startFirstPage()
    fs.getAccount()



