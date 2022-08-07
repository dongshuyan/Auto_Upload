from loguru import logger
from qbittorrentapi import Client
import time
import datetime
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys

def recordupload(torrent_file,file1,String_url,downloadurl):
    logger.info('正在记录发布的资源到'+torrent_file)
    if not os.path.exists(torrent_file):
        if 'win32' in sys.platform:
            f = open(torrent_file,'w+',encoding='utf-8-sig',errors='ignore')
        else:
            f = open(torrent_file,'w+',encoding='utf-8-sig')

        f.write('中文名,集数,发布日期,资源链接,资源下载链接\n0\n')
        f.close()

    if 'win32' in sys.platform:
        with open(torrent_file, 'r',encoding='utf-8-sig',errors='ignore') as f1:
            list1 = f1.readlines()
    else:
        with open(torrent_file, 'r') as f1:
            list1 = f1.readlines()
    while list1[-1].strip()=='':
        a=list1.pop(-1)
        del(a)
    
    try:
        num=int(list1[-1])
        a=list1.pop(-1)
        del(a)
    except:
        num=0
    if len(list1)>0:
        list1[-1]=list1[-1].strip()+'\n'

    now = datetime.datetime.now()

    filestr=''.join(list1)
    newstr=''

    newstr=newstr+file1.chinesename.replace(',',' ')+','
    if file1.pathinfo.collection==0:
        newstr=newstr+file1.episodename.zfill(2)+','
    else:
        newstr=newstr+'第'+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2)+'集 合集,'
    newstr=newstr+str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+','
    newstr=newstr+str(String_url)+','
    newstr=newstr+str(downloadurl)+'\n'

    logger.debug(newstr)

    filestr=filestr+newstr+str(num+1)+'\n'
    if 'win32' in sys.platform:
        f = open(torrent_file,'w+',encoding='utf-8-sig',errors='ignore')
    else:
        f = open(torrent_file,'w+',encoding='utf-8-sig')
    f.write(filestr)
    f.close()
    logger.info('记录完毕')

def finduploadurl(driver):
    logger.info('正在寻找发布页面链接')
    String_url = driver.current_url
    timenum=0
    while not('&uploaded' in String_url):
        timenum=timenum+1
        if timenum>10:
            logger.warning(String_url+'未找到发布页面网址')
            break
        time.sleep(1)
        String_url = driver.current_url
    String_url =String_url.split('&uploaded')[0]
    return String_url


def finddownloadurl(driver,elementstr=""):
    logger.info('正在页面下载链接')
    o = urlparse(driver.current_url)
    o = o.scheme+'://'+o.hostname+'/download.php?'
    if not elementstr=="" and len(driver.find_elements_by_xpath(elementstr))>0:
        element=driver.find_element('xpath',elementstr)
        try:
            url=element.get_attribute('href')
        except Exception as r:
            logger.error('获取网页链接失败，原因: %s' %(r))
        if o in url:
            logger.info('成功获得下载链接:'+url)
            return url
    soup = BeautifulSoup(driver.page_source,'lxml')
    for a in soup.find_all('a'):
      link = a['href']
      if o in link:
        logger.info('成功获得下载链接'+link)
        return link
    logger.warning('未找到下载链接')
    return ''


def qbseed(url,filepath,qbinfo,is_skip_checking=False,is_paused=True):
    logger.info('正在添加资源到Qbittorrent,请稍等...')
    try:
        client = Client(host=qbinfo['qburl'],username=qbinfo['qbwebuiusername'],password=qbinfo['qbwebuipassword'])
    except:
        logger.warning('Qbittorrent WEBUI登录失败,将种子添加到QB任务失败')
        return False

    logger.info('正在添加种子')
    try:
        res=client.torrents_add(urls=url,save_path=filepath,is_skip_checking=is_skip_checking,is_paused=is_paused)
    except Exception as r:
        logger.warning('添加种子进入qb出错，错误信息: %s' %(r))
        res=dict()
        #raise ValueError ('添加种子进入qbittorrent出错，程序结束')
    if 'Ok' in res:
        logger.info('已经成功添加种子')
        return True
    else:
        logger.warning('添加种子失败，返回值为:',res)
        return False

