import requests
import re
from lxml import etree
import random
import time
import pymysql
import datetime



class GetTmpMail(object):

    def __init__(self):
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


    def getRandomProxies(self):
        with open('ips_lst.txt') as f:
            ips_lst = f.read().replace('[','').replace(']','').replace("'","")
            ips_lst = ips_lst.split(',')
            ips = random.choice(ips_lst)
            ips = ips.strip()
            proxies = {'http': 'http://%s'  % ips}
            return proxies
    

    def tmpSourcePool(self, url):
        pass
    


    def tmpSourceParser(self):
        url = 'http://24mail.chacuo.net/'
        try:
            res = requests.get(url, timeout=5)
            content = etree.HTML(res.text)
            if '24mail.chacuo.net' in url:
                tmp_email = content.xpath('//*[@id="converts"]/@value')[0] + '@chacuo.net'
                
            elif 'example' in url:
                pattern = 'example'
            
            else:
                pass
        except Exception as e:
            print('request error:')
        

        return tmp_email 
    

    def insert_ips(self):
        email_account = self.tmpSourceParser()
        valid_time = 24
        check_time = datetime.datetime.now()
        try:
            sql = 'insert into tmp_mail(email_account, valid_time, check_time) values ("%s", %d, "%s")' % (email_account, valid_time, check_time)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.refresh_mysql()
            print('insert ip:', e)
            pass
    
    def delete_data(self):
        try:
            sql = 'delete from tmp_mail'
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print('delete_data', e)
            self.refresh_mysql()
    

    def run(self):
        while True:
            try:
                self.insert_ips()
                time.sleep(30)
            except:
                pass

        
    
            

if __name__ == "__main__":

    gtm = GetTmpMail()
    gtm.run()
