from loguru import logger
import undetected_chromedriver as uc 
import ssl
import time
from function_controler import func_maxtime

ssl._create_default_https_context = ssl._create_unverified_context
uc.TARGET_VERSION = 91


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
            self.driver = func_maxtime(func=newweb,args=(options,),limit_time=10,kill=True,allow_log=True)
            #self.driver = uc.Chrome(use_subprocess=True,options=options)
        except Exception as r:
            logger.warning('新建浏览器发生错误，错误信息: %s' %(r))
            self.browser=False

        if self.driver==None:
            logger.warning('新建浏览器超时')
            self.browser=False

        if self.browser:
            self.driver.set_page_load_timeout(self.waittime)

    def __del__(self):
        if self.browser:
            logger.info('正在关闭'+self.site.sitename+'站点的浏览器')
            try:
                self.driver.quit()
            except Exception as r:
                logger.warning('关闭浏览器发生错误，错误信息: %s' %(r))

    def wait_page(self):
        try:
            useritem=self.driver.find_elements_by_name('username')
            fileitem=self.driver.find_elements_by_name('file')
        except Exception as r:
            logger.warning('寻找页面组件发生错误，错误信息: %s' %(r))
            return False

        trynum=0
        while len(useritem)+len(fileitem)<=0:
            trynum=trynum+1
            if trynum>15:
                return False
            time.sleep(1)
            try:
                useritem=self.driver.find_elements_by_name('username')
                fileitem=self.driver.find_elements_by_name('file')
            except Exception as r:
                logger.warning('寻找页面组件发生错误，错误信息: %s' %(r))
                return False
        return True

    def login_account(self):
        return -1

    def login_cookie(self):
        try:
            self.driver.delete_all_cookies()
        except Exception as r:
            logger.warning('清除cookie发生错误，错误信息: %s' %(r))

        if len(self.site.cookie)<=0:
            print('未找到cookie,将尝试使用账号密码登录,请稍后...')
            return self.login_account()
            

        logger.info('正在尝试使用cookie登录'+self.site.sitename+'站点,请稍后...')
        try:
            self.driver.get(self.site.loginurl)
        except Exception as r:
            logger.warning('打开登录页面发生错误，错误信息: %s' %(r))
            return -1

        if len(self.driver.find_elements_by_name('username'))<=0:
            self.driver.execute_script("window.scrollBy(0,300)")

        if not self.wait_page():
            logger.warning('登录页面加载失败')
            return -1

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

        if not self.wait_page():
            logger.warning('发布页面加载失败')
            return -1

        try:
            fileitem=self.driver.find_elements_by_class_name('file')
        except Exception as r:
            logger.warning('打开发布页面发生错误，错误信息: %s' %(r))

        if len(fileitem)>0:
            print('登录站点成功！')
            self.login=True
            return 1
        else:
            print('cookie登录站点失败,将尝试使用账号密码登录,请稍后...')
            return self.login_account()
        return-1


        