from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import name_generator
import random
import pymysql
from user_agents import agents
import re
import datetime


class FbAccessToken(object):

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
    

    def getRandomIp(self):
        with open('ips_lst.txt') as f:
            ips_lst = f.read().replace('[','').replace(']','').replace("'","")
            ips_lst = ips_lst.split(',')
            return random.choice()

    

    def mobileRegister(self):
        try:
            driver = webdriver.PhantomJS()
            url = 'https://www.facebook.com/'
            driver.get(url)
            # first register page
            mailAddress = self.createTmpEmail()
            driver.find_element_by_xpath('//input[@name="email"]').send_keys(mailAddress)
            driver.find_element_by_xpath('//input[@name="pass"]').send_keys('zhonghong')
            driver.find_element_by_xpath('//input[@name="sign_up"]').click()
            # confirm page
            firstname, lastname = name_generator.nameGenerator()
            driver.find_element_by_xpath('//input[@name="firstname"]').send_keys(firstname)
            driver.find_element_by_xpath('//input[@name="lastname"]').send_keys(lastname)
            driver.find_element_by_xpath('//input[@name="reg_email__"]').send_keys(mailAddress)
            driver.find_element_by_xpath('//input[@name="sex"]').click()
            driver.find_element_by_xpath('//input[@name="reg_passwd__"]').send_keys('izhonghong')
            driver.find_element_by_xpath('//input[@name="submit"]').click()
            # confirm birthday
            driver.find_element_by_xpath('//input[@name="submit"]').click()
            
        except Exception as e:
            print('register error', e)
        finally:
            driver.quit()
            time.sleep(60)

        self.pcLogin(mailAddress)

       

    def pcLogin(self, mailAddress):

        try:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2995.0 Safari/537.36')
            # dcap["phantomjs.page.settings.userAgent"] = (random.choice(agents))
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            url = 'https://www.facebook.com/'
            driver.get(url)
            driver.find_element_by_xpath('//input[@name="email"]').send_keys(mailAddress)
            driver.find_element_by_xpath('//input[@name="pass"]').send_keys('izhonghong')
            driver.find_element_by_xpath('//input[@value="Log In"]').click()
            # enter homepage
            driver.find_element_by_xpath('//a[@accesskey="2"]').click()
            # get access_token
            content = driver.page_source
            access_token = re.search('access_token:".*?",', content).group()
            access_token = access_token.replace("access_token:","")
            access_token = access_token.replace('"','')
            access_token = access_token.replace(',','')

            driver.quit()

            self.insert2mysql(access_token)

        except Exception as e:
            print(e)
    


    def insert2mysql(self, access_token):

        check_time = datetime.datetime.now()
        try:
            sql = 'insert into fb_access_token (access_token, check_time) values ("%s", "%s")' % (access_token, check_time)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.refresh_mysql()
            print('insert ip:', e)
            pass
    

    def delete_data(self):
        try:
            sql = 'delete from fb_access_token where valid_tg is not NULL'
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print('delete_data', e)
            self.refresh_mysql()
        
    
    def createTmpEmail(self):

        try:
            sql = 'select email_account from tmp_mail where used is NULL LIMIT 1'
            self.cursor.execute(sql)
            mailAddress = self.cursor.fetchone()[0]
        except Exception as e:
            print(e)
        
        try:
            sql = 'update tmp_mail set used = 1 where email_account = "%s"' % mailAddress
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)

        return mailAddress

    
    def snapshot(self, driver):
        driver.save_screenshot('aa.png')


    def pageSource(self, page_source):
        # driver.page_source
        with open('register.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
    

    def run(self):
        while True:
            try:
                self.mobileRegister()
            except Exception as e:
                print(e)
            



if __name__ == "__main__":

    fat = FbAccessToken()
    fat.delete_data()
    #  0 * * * *  python3  /root/overseas_crawler/facebook/crontab_delete_token.py