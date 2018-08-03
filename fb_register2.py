from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
import name_generator
import random
import pymysql
from user_agents import agents
import re
import datetime
import requests


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
            print 'refresh:', e
            time.sleep(10)
    

    def getRandomIpFromWs(self):
        ips_lst = [] 
        url = 'http://119.145.230.3:9999/zhonghong/proxy/abroad'
        res = requests.get(url, timeout=3)
        content = res.text.replace('\\', '')
        lst = re.findall('proxy_ip.*?proxy_port.*?,', content)
        for i in lst:
            i = i.replace('"','').replace('proxy_ip:','').replace('proxy_port:','')
            i = i.split(',')
            ips = i[0] + ':' + i[1]
            ips_lst.append(ips)
        return random.choice(ips_lst)

    

    def checkProxyLogin(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=192.168.2.39:808') 
        driver = webdriver.Chrome(chrome_options = options)
        url = 'https://www.facebook.com/'
        driver.get(url)
        time.sleep(10)
        driver.quit()


    def PcRegister(self):
        try:
            # 参数配置
            options = webdriver.ChromeOptions()
            # 禁止弹窗
            prefs = {
                'profile.default_content_setting_values' :
                    {
                    'notifications' : 2
                    }
            }
            options.add_experimental_option('prefs',prefs)
            # 随机请求头
            headers = 'user-agent=' + random.choice(agents)
            options.add_argument(headers)
            # 命令行模式
            # options.add_argument('-headless')
            # options.add_argument('--disable-gpu')
            # 添加代理
            ips = '192.168.2.39:808'
            options.add_argument('--proxy-server=%s' % ips) 
            # 启动浏览器
            driver = webdriver.Chrome(chrome_options=options)

            # 开始请求
            url = 'https://www.facebook.com/'
            driver.get(url)

            # 随机生成姓名
            firstname, lastname = name_generator.nameGenerator()
            driver.find_element_by_xpath('//input[@name="lastname"]').send_keys(lastname)
            time.sleep(2)
            driver.find_element_by_xpath('//input[@name="firstname"]').send_keys(firstname)
            time.sleep(5)

            # 输入邮箱
            mailAddress = self.createTmpEmail()
            driver.find_element_by_xpath('//input[@name="reg_email__"]').send_keys(mailAddress)
            time.sleep(5)
            driver.find_element_by_xpath('//input[@name="reg_email_confirmation__"]').send_keys(mailAddress)
            time.sleep(2)

            # 确定密码
            driver.find_element_by_xpath('//input[@name="reg_passwd__"]').send_keys('izhonghong')
            time.sleep(2)

            # 确定日期
            Select(driver.find_element_by_id("month")).select_by_value(str(random.randint(3,12)))
            time.sleep(3)
            Select(driver.find_element_by_id("day")).select_by_value(str(random.randint(1,30)))
            time.sleep(3)


            # 确定性别
            driver.find_element_by_xpath('//input[@name="sex"]').click()
            time.sleep(3)

            # 注册按钮
            driver.find_element_by_xpath('//button[@name="websubmit"]').click()
            now = datetime.datetime.now()
            print now, '  注册成功!,账号为: ', mailAddress

            # 被识别则退出
            if 'checkpoint' in url:
                return

            # 进入主页
            time.sleep(10)
            driver.find_element_by_xpath('//a[@accesskey="2"]').click()
            time.sleep(60)

            # 被识别则退出
            url = driver.current_url
            if 'checkpoint' in url:
                return
            
            # 刷新主页
            driver.get(url)
            time.sleep(10)

            content = driver.page_source
            access_token = re.search('access_token:".*?",', content).group()
            access_token = access_token.replace('"','')
            access_token = access_token.replace(',','')
            access_token = access_token.replace("access_token:","")

            now = datetime.datetime.now()
            print now, '  获取token成功!  ', access_token

            self.insert2mysql(access_token)
            
        except Exception as e:
            now = datetime.datetime.now()
            print now, '  注册失败,模拟失败'
            driver.delete_all_cookies()
            driver.quit()
            return

        finally:
            driver.delete_all_cookies()
            driver.quit()
    

    def mobileRegister(self):

        try:

            # 参数配置
            options = webdriver.ChromeOptions()
            # 禁止弹窗
            prefs = {
                'profile.default_content_setting_values' :
                    {
                    'notifications' : 2
                    }
            }
            options.add_experimental_option('prefs',prefs)
            # 随机请求头
            # headers = 'user-agent=' + random.choice(agents)
            # options.add_argument(headers)
            # 命令行模式
            # options.add_argument('-headless')
            # options.add_argument('--disable-gpu')
            # 添加代理
            ips = '192.168.2.39:808'
            options.add_argument('--proxy-server=%s' % ips) 
            # 启动浏览器
            driver = webdriver.Chrome(chrome_options=options)

            # 开始请求
            url = 'https://m.facebook.com/'
            driver.get(url)

            # 开始注册
            driver.find_element_by_xpath('//a[@id="signup-button"]').click()
            time.sleep(3)

            # 随机生成姓名
            firstname, lastname = name_generator.nameGenerator()
            driver.find_element_by_xpath('//input[@name="lastname"]').send_keys(lastname)
            time.sleep(2)
            driver.find_element_by_xpath('//input[@name="firstname"]').send_keys(firstname)
            time.sleep(2)
            driver.find_element_by_xpath('//button[@data-sigil="touchable multi_step_next"]').click()
            time.sleep(3)

            # 确定日期
            Select(driver.find_element_by_id("month")).select_by_value(str(random.randint(3,12)))
            time.sleep(3)
            Select(driver.find_element_by_id("day")).select_by_value(str(random.randint(1,30)))
            time.sleep(3)
            driver.find_element_by_xpath('//button[@data-sigil="touchable multi_step_next"]').click()
            time.sleep(3)

            # 切换到邮箱注册
            driver.find_element_by_xpath('//a[@data-sigil="switch_phone_to_email"]').click()
            time.sleep(3)

            # 输入邮箱
            mailAddress = self.createTmpEmail()
            driver.find_element_by_xpath('//input[@name="reg_email__"]').send_keys(mailAddress)
            time.sleep(3)
            driver.find_element_by_xpath('//button[@data-sigil="touchable multi_step_next"]').click()
            time.sleep(3)

            # 确定性别
            driver.find_element_by_xpath('//input[@name="sex"]').click()
            time.sleep(3)
            driver.find_element_by_xpath('//button[@data-sigil="touchable multi_step_next"]').click()
            time.sleep(3)

            # 确定密码
            driver.find_element_by_xpath('//input[@name="reg_passwd__"]').send_keys('izhonghong')
            time.sleep(5)

            # 注册按钮
            driver.find_element_by_xpath('//button[@name="submit"]').click()
            time.sleep(5)

            # 不保存密码
            driver.find_element_by_xpath('//a[@role="button"]').click()
            time.sleep(8)

            # 转换成pc模式
            pcUrl = driver.current_url.replace("m.", "")
            driver.get(pcUrl)

        except Exception as e:
            print e
            driver.delete_all_cookies()
            driver.quit()
        finally:
            driver.delete_all_cookies()
            driver.quit()





    def insert2mysql(self, access_token):

        check_time = datetime.datetime.now()
        try:
            sql = 'insert into fb_access_token (token, check_time) values ("%s", "%s")' % (access_token, check_time)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.refresh_mysql()
            print 'insert ip:', e
            pass
    

    def delete_data(self):
        try:
            sql = 'delete from fb_access_token where valid_tag is not NULL'
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print 'delete_data', e
            self.refresh_mysql()
        
    
    def createTmpEmail(self):

        try:
            sql = 'select email_account from tmp_mail where used is NULL LIMIT 1'
            self.cursor.execute(sql)
            mailAddress = self.cursor.fetchone()[0]
        except Exception as e:
            print e

        try:
            sql = 'update tmp_mail set used = 1 where email_account = "%s"' % mailAddress
            self.cursor.execute(sql)
            self.db.commit()
            now = datetime.datetime.now()
        except Exception as e:
            print e

        now = datetime.datetime.now()
        return mailAddress

    
    def snapshot(self, driver):
        driver.save_screenshot('aa.png')


    def pageSource(self, page_source):
        # driver.page_source
        with open('register_log.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
    

    def run(self):
        while True:
            try:
                self.PcRegister()
                time.sleep(60)
            except Exception as e:
                pass
            



if __name__ == "__main__":

    fat = FbAccessToken()
    fat.run()
    # fat.mobileRegister()

    
    
