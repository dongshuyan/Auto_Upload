from loguru import logger
import json
import os.path

class site(object):
    def __init__(self,sitename,sitedict):
        self.sitename   = sitename
        self.exist_cookie=False
        self.exist_password=False
        self.uplver =1
        self.enable =0
        self.check = False

        attr=['loginurl','uploadurl']
        for item in attr:
            if not item in sitedict  or sitedict[item]==None:
                logger.error('未识别'+sitename+' 站点的'+item+'信息')
                raise ValueError ('未识别'+sitename+' 站点的'+item+'信息')
            else:
                exec('self.'+item+'=sitedict[item]')

        self.url='/'.join(self.loginurl.split('/')[:3])

        try:
            self.uplver =int(sitedict['uplver'])
        except:
            logger.warning(sitename+'站点匿名发布uplver信息填错错误，已设置为1:默认匿名发布')
            self.uplver =1
            sitedict['uplver']=1

        if not (self.uplver==0 or self.uplver==1):
            logger.warning(sitename+'站点匿名发布uplver信息填错错误，已设置为1:默认匿名发布')
            self.uplver =1
            sitedict['uplver']=1


        try:
            self.enable =int(sitedict['enable'])
        except:
            logger.warning(sitename+'站点enable信息填错错误，已设置为0:关闭')
            self.enable =0
            sitedict['enable']=0

        if not (self.enable==0 or self.enable==1):
            logger.warning(sitename+'站点匿名发布enable信息填错错误，已设置为0:关闭')
            self.enable =0
            sitedict['enable']=0
        
        if 'tracker' in sitedict and not sitedict['tracker']==None:
            self.tracker = sitedict['tracker']
        else:
            sitedict['tracker']='https://tracker.pterclub.com/announce'

        if 'cookiefile' in sitedict :
            if  os.path.exists(sitedict['cookiefile']):
                self.cookiefile = sitedict['cookiefile']
                self.cookie=json.load(open(self.cookiefile,'r',encoding="utf-8"))
                self.exist_cookie=True
            else:
                self.cookiefile = sitedict['cookiefile']
                self.cookie=[]
                self.exist_cookie=False
        else:
            self.cookiefile=None
            self.cookie=[]
            self.exist_cookie=False

        if 'check' in sitedict :
            if str(sitedict['check']=='1'):
                self.check=True
            else:
                self.check=False
        if 'username' in sitedict and not sitedict['username']==None and 'password' in sitedict and not sitedict['password']==None:
            self.username   = sitedict['username']
            self.password   = sitedict['password']
            self.exist_password=True

        if self.enable==1 and (not self.exist_cookie and not self.exist_password):
            logger.error('未找到'+sitename+' 站点的cookie信息以及用户名密码信息，请至少填写一个')
            raise ValueError ('未找到'+sitename+' 站点的cookie信息以及用户名密码信息，请至少填写一个')

        if self.exist_cookie:
            expiry=2147483647
            for cookieitem in self.cookie:
                if 'expirationDate' in cookieitem:
                    expiry=int(float(cookieitem['expirationDate']))
                    break
            for cookieitem in self.cookie:
                itemlist=[]
                for item in cookieitem:
                    if cookieitem[item]=='unspecified':
                        itemlist.append(item)
                for item in itemlist:
                    cookieitem.pop(item)
                if 'expirationDate' in cookieitem:
                    cookieitem['expiry']=int(float(cookieitem['expirationDate']))
                    cookieitem.pop('expirationDate')
                else:
                    cookieitem['expiry']=expiry
                if 'hostOnly' in cookieitem:
                    cookieitem.pop('hostOnly')
                if 'session' in cookieitem:
                    cookieitem.pop('session')
                if 'storeId' in cookieitem:
                    cookieitem.pop('storeId')
                if 'id' in cookieitem:
                    cookieitem.pop('id')
                if 'sameSite' in cookieitem :#and sitename=='ssd':
                    cookieitem.pop('sameSite')
    def print(self):

        print('Site info:')
        print('sitename:'  ,self.sitename  )
        print('enable:'    ,self.enable    )
        print('url:'       ,self.url       )
        print('loginurl:'  ,self.loginurl  )
        print('uploadurl:' ,self.uploadurl )
        print('tracker:'   ,self.tracker   )
        if self.exist_password:
            print('username:'  ,self.username  )
            print('password:'  ,self.password  )
        else:
            print('username:未设置或未识别')
            print('password:未设置或未识别')
        if self.exist_cookie:
            print('cookiefile:',self.cookiefile)
        else:
            print('cookiefile:未设置或未识别')
        print('')

def makesites(siteinfo):
    sites=dict()
    for item in siteinfo:
        sites[item]=site(item,siteinfo[item])
    return sites








