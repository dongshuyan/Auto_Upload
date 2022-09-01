from loguru import logger
from qbittorrentapi import Client
import time
import datetime
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
import re
from selenium.webdriver.common.by import By

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
        num=int(list1[-1].replace(',','').strip())
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
    if not ('anime' in file1.pathinfo.type.lower() or 'tv' in file1.pathinfo.type.lower()) or file1.pathinfo.collection==0:
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
    logger.info('正在寻找页面下载链接')
    o = urlparse(driver.current_url)
    o = o.scheme+'://'+o.hostname+'/download.php?'
    if not elementstr=="" and len(driver.find_elements(By.XPATH,elementstr))>0:
        element=driver.find_element('xpath',elementstr)
        try:
            url=element.get_attribute('href')
        except Exception as r:
            logger.error('获取网页链接失败，原因: %s' %(r))
        if o in url:
            logger.info('成功获得下载链接:'+url)
            return url
    logger.warning('未通过标签找到下载链接，正在直接通过页面查找...')
    soup = BeautifulSoup(driver.page_source,'lxml')
    for a in soup.find_all('a'):
        link=''
        try:
            link = a['href']
        except:
            logger.warning('该a标签未找到href属性')
        if o in link:
            logger.info('成功获得下载链接'+link)
            return link

    for a in soup.find_all('a'):
        link=''
        try:
            link = a['href']
        except:
            logger.warning('该a标签未找到href属性')
        if len(re.findall(r'download.php\?id=[0-9]+&',link))>0:
            o = urlparse(driver.current_url)
            if link.startswith('download.php'):
                link=o.scheme+'://'+o.hostname+'/'+link
            logger.info('成功获得下载链接'+link)
            return link


    logger.warning('未找到下载链接')
    if '已存在' in driver.page_source:
        logger.warning('该种子已存在')
        return '已存在'
    return ''


def qbseed(url,filepath,qbinfo,is_skip_checking=False,is_paused=True,category=None):
    logger.info('正在添加资源到Qbittorrent,请稍等...')

    if int(qbinfo['start'])==1:
        is_paused=False
    else:
        is_paused=True

    try:
        client = Client(host=qbinfo['qburl'],username=qbinfo['qbwebuiusername'],password=qbinfo['qbwebuipassword'])
    except:
        logger.warning('Qbittorrent WEBUI登录失败,将种子添加到QB任务失败')
        return False

    logger.info('正在登录Qbittorrent WEBUI')
    try:
        client.auth_log_in()
    except:
        logger.warning('Qbittorrent WEBUI信息错误，登录失败，请检查au.yaml文件里的url、用户名、密码')
        return False
    logger.info('成功登录Qbittorrent WEBUI')

    tor_num=len(client.torrents_info())
    tor_num_new=tor_num
    trynum=0
    while tor_num_new==tor_num:
        trynum=trynum+1
        if trynum>12:
            logger.warning('添加种子失败,种子下载链接为:'+url+'   请自行手动添加')
            return False
        logger.info('正在第'+str(trynum)+'次添加种子')
        try:
            res=client.torrents_add(urls=url,save_path=filepath,is_skip_checking=is_skip_checking,is_paused=is_paused,use_auto_torrent_management=None,category=category)
        except Exception as r:
            logger.warning('添加种子进入qb出错，错误信息: %s' %(r))
            continue
            #raise ValueError ('添加种子进入qbittorrent出错，程序结束')
        if 'Ok' in res:
            logger.info('返回值显示成功添加种子')
        else:
            logger.warning('添加种子失败，返回值为:',res)
        time.sleep(1)
        tor_num_new=len(client.torrents_info())
        if tor_num_new==tor_num:
            time.sleep(5)
            tor_num_new=len(client.torrents_info())

    logger.info('已经成功添加种子')

    if 'lemonhd' in url:
        logger.info('发现lemonhd的种子,正在更改tracker...')
        addtime=0
        torrentlist=client.torrents.info()
        for item in torrentlist:
            if item.added_on>addtime:
                addtime=item.added_on
                to=item
        for item in to.trackers:
            if 'url' in item and 'leaguehd' in item['url']:
                tracker=item['url']
                if 'http:' in tracker:
                    try:
                        to.edit_tracker(orig_url=tracker,new_url=tracker.replace('http:','https:'))
                    except Exception as r:
                        logger.error('更改tracker失败，原因: %s' %(r))

    return True
