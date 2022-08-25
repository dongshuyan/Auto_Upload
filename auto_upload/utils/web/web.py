from loguru import logger
import undetected_chromedriver as uc 
import ssl
import time
from function_controler import func_maxtime
import ddddocr
import os
import platform
from PIL import Image
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

ssl._create_default_https_context = ssl._create_unverified_context
uc.TARGET_VERSION = 91

def showpic(file):
    opener ="open" if sys.platform =="darwin" else"xdg-open"
    subprocess.call([opener, file])

def newweb(options):
    return uc.Chrome(use_subprocess=True,options=options)

class web(object):
    def __init__(self,site,headless=False):
        logger.info('正在新建浏览器')
        self.browser=True
        self.waittime=60
        self.site=site
        self.login=False
        self.driver=None
        self.headless=headless
        options = uc.ChromeOptions()
        prefs = {
            "download.prompt_for_download": False,
            "download_restrictions": 3,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-desktop-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--no-first-run')
        options.add_argument('--no-service-autorun')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--password-store=basic')
        if headless:
            options.add_argument('--headless')
        try:
            self.driver = func_maxtime(func=newweb,args=(options,),limit_time=20,kill=True,allow_log=True)
            #self.driver = uc.Chrome(use_subprocess=True,options=options)
        except Exception as r:
            logger.warning('新建浏览器发生错误，错误信息: %s' %(r))
            self.browser=False

        if self.driver==None:
            logger.warning('新建浏览器超时')
            self.browser=False

        if self.browser:
            self.driver.set_page_load_timeout(self.waittime)

        self.login_element='menu'
        if self.site.sitename=='hare':
            self.login_element='layui-nav'
        elif self.site.sitename=='ttg':
            self.login_element='smallfont'
        elif self.site.sitename=='pttime':
            self.login_element='selected'
        elif self.site.sitename=='98t':
            self.login_element='ddpc_sign_btna'


    def __del__(self):
        if self.browser:
            logger.info('正在关闭'+self.site.sitename+'站点的浏览器')
            try:
                self.driver.quit()
            except Exception as r:
                logger.warning('关闭浏览器发生错误，错误信息: %s' %(r))

    def writecookie(self):
        try:
            cookiedata=self.driver.get_cookies()
        except Exception as r:
            logger.warning('获取站点cookie发生错误，错误信息: %s' %(r))
            return
        self.site.cookie=cookiedata
        self.site.exist_cookie=True

        if (not 'cookiefile' in dir(self.site) ) or self.site.cookiefile==None or self.site.cookiefile=='':
            logger.warning('未找到cookie文件路径，无法写入')
            return 
        cookiefile=self.site.cookiefile
        
        f=open(cookiefile, "w+", encoding='utf-8')
        f.write('[')
        cookienum=len(cookiedata)
        for i in range(len(cookiedata)):
            if i!=0:
                f.write(',')
            f.write('\n{\n')
            itemnum=len(cookiedata[i])
            itemtime=0
            for item in cookiedata[i]:
                itemtime=itemtime+1
                f.write('    "'+item+'": '+(type(cookiedata[i][item])==str)*'"'+str(cookiedata[i][item]).replace('True','true').replace('False','false')+(type(cookiedata[i][item])==str)*'"')
                if itemtime!=itemnum:
                    f.write(',')
                f.write('\n')
            f.write('}')

        f.write('\n]')
        f.close()
        logger.warning('已成功将站点'+self.site.sitename+'的cookie信息写入文件'+cookiefile)



    def wait_page(self):
        try:
            #useritem=self.driver.find_elements(By.NAME,'username')
            #fileitem=self.driver.find_elements(By.NAME,'file')
            useritem=self.driver.find_elements(By.NAME,'username')
            #fileitem=self.driver.find_elements(By.NAME,'file')
            fileitem=self.driver.find_elements(By.CLASS_NAME,self.login_element)
        except Exception as r:
            logger.warning('寻找页面组件发生错误，错误信息: %s' %(r))
            return 0

        if 'not found' in self.driver.page_source.lower():
            return -2
        trynum=0
        while len(useritem)+len(fileitem)<=0:
            trynum=trynum+1
            if trynum>15:
                return 0
            time.sleep(1)
            try:
                useritem=self.driver.find_elements(By.NAME,'username')
                #fileitem=self.driver.find_elements(By.NAME,'file')
                fileitem=self.driver.find_elements(By.CLASS_NAME,self.login_element)
            except Exception as r:
                logger.warning('寻找页面组件发生错误，错误信息: %s' %(r))
                return 0
        return 1

    
    def login_account(self,autologin=True):
        img_login=0
        try:
            self.driver.delete_all_cookies()
        except Exception as r:
            logger.warning('清除cookie发生错误，错误信息: %s' %(r))   

        logger.info('正在尝试使用账号密码登录站点...')

        if not ('username' in dir(self.site) and self.site.username!=None and 'password' in  dir(self.site) and self.site.password!=None): 
            logger.warning('登录失败，失败原因:站点'+self.site.sitename+'用户名密码信息不全，请检查配置文件au.yaml')
            return -1

        try:
            self.driver.get(self.site.loginurl)
        except Exception as r:
            logger.warning('打开登录页面发生错误，错误信息: %s' %(r))

        if len(self.driver.find_elements(By.NAME,'username'))<=0:
            self.driver.execute_script("window.scrollBy(0,300)")

        if self.wait_page()!=1:
            logger.warning('登录页面加载失败')
            return -1

        try:
            self.driver.find_elements(By.NAME,'username')[0].send_keys(self.site.username)
            self.driver.find_elements(By.NAME,'password')[0].send_keys(self.site.password)
        except Exception as r:
            logger.warning('输入用户名密码发生错误，错误信息: %s' %(r))
            return -1

        if self.site.sitename=='ssd':
            imgs=self.driver.find_elements(By.XPATH,'/html/body/section/main/div/form/div[3]/span[1]/img')
        elif self.site.sitename=='hare':
            imgs=self.driver.find_elements(By.XPATH,'/html/body/div[3]/form[2]/div[3]/div[2]/img')
        else:
            imgs=self.driver.find_elements(By.XPATH,'/html/body/table[2]/tbody/tr/td/form[2]/table/tbody/tr[4]/td[2]/img')

        if len(imgs)>0:
            logger.info('遇到验证码，请稍等...')
            if self.headless==True:
                logger.warning('检测到目前正在后台运行，无法识别验证码，正常尝试重新登录,请稍等')
                return -1
            img_login=1
            #image_code_name=os.path.join(self.basic['screenshot_address'],'code.png')
            image_code_name=os.path.join(os.getcwd(),'code.png')
            if os.path.exists(image_code_name):
                logger.info('已存在验证码图片，正在删除'+image_code_name)
                try:
                    os.remove(image_code_name)
                except Exception as r:
                    logger.warning('删除图片发生错误: %s' %(r))
            try:
                self.driver.save_screenshot(image_code_name)
            except Exception as r:
                logger.info('保存图片发生错误，错误信息: %s' %(r))
            img_element = imgs[0]
            left = img_element.location['x']
            top = img_element.location['y']
            right = (img_element.location['x'] + img_element.size['width']) 
            bottom = (img_element.location['y'] + img_element.size['height']) 
            if platform.system()=='Darwin':
                left=left*2
                top=top*2
                right=right*2
                bottom=bottom*2
            logger.info('已获取位置')
            im = Image.open(image_code_name)
            im = im.crop((left, top, right, bottom))
            im.save(image_code_name)
            with open(image_code_name, 'rb') as f:
                image = f.read()  
            if autologin==False:
                autologin=int(input('是否使用OCR识别验证码,0否1是:'))
            if autologin==True:
                ocr = ddddocr.DdddOcr(show_ad=False,old=True)
                data_ocr = ocr.classification(image)
            else:
                showpic(image_code_name)
                data_ocr=input('请输入文件所示验证码:') 
        

            if os.path.exists(image_code_name):
                logger.info('正在删除验证码图片'+image_code_name)
                try:
                    os.remove(image_code_name)
                except Exception as r:
                    logger.warning('删除图片发生错误: %s' %(r))

            try:
                self.driver.find_elements(By.NAME,'imagestring')[0].send_keys(data_ocr)
            except Exception as r:
                logger.info('输入验证码发生错误: %s' %(r)) 
                #return -1      

        logger.info('正在点击登录...')

        submitxpath='/html/body/table[2]/tbody/tr/td/form[2]/table/tbody/tr[10]/td/input[1]'
        if self.site.sitename=='hdyu':
            submitxpath='/html/body/table[2]/tbody/tr/td/form[2]/table/tbody/tr[7]/td/input[1]'
        elif self.site.sitename=='pter':
            time.sleep(3)
        elif self.site.sitename=='hare':
            submitxpath='/html/body/div[3]/form[2]/div[8]/button[1]'
        elif self.site.sitename=='tjupt':
            submitxpath='/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[5]/td/input[1]'

        try:
            if len(self.driver.find_elements(By.XPATH,submitxpath))>0:
                logger.info('找到登录按键')
                self.driver.find_element(By.XPATH,submitxpath).click()
        except Exception as r:
            logger.info('点击登录发生错误: %s' %(r)) 
        
        try:
            self.driver.get(self.site.uploadurl)
        except Exception as r:
            logger.warning('打开登录页面发生错误，错误信息: %s' %(r))
            return -1

        if self.wait_page()!=1:
            logger.warning('登录页面加载失败')
            return -1

        try:
            #fileitem=self.driver.find_elements(By.CLASS_NAME,'file')
            fileitem=self.driver.find_elements(By.CLASS_NAME,self.login_element)
        except Exception as r:
            logger.info('打开发布页面发生错误，错误信息: %s' %(r))

        if len(fileitem)>0:
            logger.info('登录站点成功！')
            self.login=True
            self.writecookie()
            return 1
        else:
            if autologin==False or img_login==0:
                logger.warning('站点登录失败')
                return -1
            logger.info('自动识别验证码登陆失败,请手动输入验证码重试...')
            return self.login_account(autologin=False)
        return -1


    def login_cookie(self):
        try:
            self.driver.delete_all_cookies()
        except Exception as r:
            logger.warning('清除cookie发生错误，错误信息: %s' %(r))

        if self.site.exist_cookie==False or len(self.site.cookie)<=0:
            logger.warning('未找到cookie,将尝试使用账号密码登录,请稍后...')
            return self.login_account()
            
        logger.info('正在尝试使用cookie登录'+self.site.sitename+'站点,请稍后...')

        try:
            o = urlparse(self.site.loginurl)
            o = o.scheme+'://'+o.hostname+'/asddsa000.php'
            self.driver.get(o)
        except Exception as r:
            logger.warning('导入登录页面域名发生错误，错误信息: %s' %(r))
            #return -1
        '''
        if len(self.driver.find_elements(By.NAME,'username'))<=0:
            self.driver.execute_script("window.scrollBy(0,300)")
        '''
        if self.wait_page()==0:
            logger.warning('登录页面加载失败')
            #return -1

        try:
            self.driver.delete_all_cookies()
        except Exception as r:
            logger.warning('清除cookie发生错误，错误信息: %s' %(r))

        logger.info('正在导入cookie...')
        for site_cookie in self.site.cookie:
            try:
                self.driver.add_cookie(site_cookie)
            except Exception as r:
                logger.warning('导入冗余cookie，错误信息: %s' %(r))
        logger.info('已经成功导入cookie')
        logger.info('正在尝试打开发布页面...')
        try:
            self.driver.get(self.site.uploadurl)
        except Exception as r:
            logger.warning('打开发布页面发生错误，错误信息: %s' %(r))

        if self.wait_page()!=1:
            logger.warning('发布页面加载失败')
            return -1

        try:
            #fileitem=self.driver.find_elements(By.CLASS_NAME,'file')
            fileitem=self.driver.find_elements(By.CLASS_NAME,self.login_element)
        except Exception as r:
            logger.warning('寻找登录成功组件发生错误，错误信息: %s' %(r))

        if len(fileitem)>0:
            logger.info('登录站点成功！')
            self.login=True
            return 1
        else:
            logger.warning('cookie登录站点失败,将尝试使用账号密码登录,请稍后...')
            return self.login_account()
        return-1


        