from auto_upload.utils.pathinfo.pathinfo import findnum
import os
from loguru import logger
import time
import requests
import re
import json
import sys
from auto_upload.utils.img_upload.imgupload import img_upload

def deletetorrent(delpath=''):
    if delpath=='':
        delpath = os.path.dirname(os.path.abspath(__file__))
    logger.info('正在清除此文件夹下所有种子文件:'+delpath)
    ls = os.listdir(delpath)
    for i in ls:
        c_path = os.path.join(delpath, i)
        if (os.path.isfile(c_path)) and (os.path.splitext(i)[1].lower()== ('.torrent')  or i.startswith('.')):
            logger.info('正在删除文件:'+c_path+'...')
            os.remove(c_path)

def changename(path):
    if not 'win' in sys.platform:
        return path
    else:
        return '/cygdrive/'+path.replace('\\','/').replace(':','')
def mktorrent_win(filepath,torrentname,tracker="https://announce.leaguehd.com/announce.php"):
    cwd=os.getcwd()
    newcwd=os.path.dirname(filepath)
    os.chdir(newcwd)
    if os.path.isdir(filepath):
        logger.info('检测到路径制种，将先删除掉路径里面所有种子文件(torrent后缀)以及隐藏文件（.开头的文件）...')
        deletetorrent(filepath) 
    logger.info('即将开始制作种子...')
    if os.path.exists(torrentname):
        logger.info('已存在种子文件，正在删除'+torrentname)
        try:
            os.remove(torrentname)
        except Exception as r:
            logger.error('删除种子发生错误: %s' %(r))
    logger.info('正在制作种子:'+filepath)
    order='mktorrent -v -p -f -l 24 -a '+tracker+' -o \"'+changename(torrentname)+ '\" \"'+os.path.basename(filepath)+'\"'+''
    logger.info(order)
    os.system(order)
    logger.info('已完成制作种子'+torrentname)
    os.chdir(cwd)

def mktorrent(filepath,torrentname,tracker="https://announce.leaguehd.com/announce.php"):
    if 'win32' in sys.platform:
        mktorrent_win(filepath,torrentname,tracker)
        return 
    if os.path.isdir(filepath):
        logger.info('检测到路径制种，将先删除掉路径里面所有种子文件(torrent后缀)以及隐藏文件（.开头的文件）...')
        deletetorrent(filepath) 
    logger.info('即将开始制作种子...')
    if os.path.exists(torrentname):
        logger.info('已存在种子文件，正在删除'+torrentname)
        try:
            os.remove(torrentname)
        except Exception as r:
            logger.error('删除种子发生错误: %s' %(r))
    logger.info('正在制作种子:'+filepath)
    order='mktorrent -v -p -f -l 24 -a '+tracker+' -o \"'+torrentname+ '\" \"'+filepath+'\"'+' > /dev/null'
    #logger.info(order)
    os.system(order)
    logger.info('已完成制作种子'+torrentname)


def get_video_duration(video_path: str):
    ext = os.path.splitext(video_path)[-1]
    if ext != '.mp4' and ext != '.avi' and ext != '.flv'and ext != '.ts'and ext != '.mkv':
        raise Exception('format not support')
    ffprobe_cmd = 'ffprobe -i "'+video_path+'" -show_entries format=duration -v quiet -of csv="p=0"'
    a=os.popen(ffprobe_cmd)
    duration_info = float(a.read())
    #duration_info = float(a.buffer.read().decode('utf-8'))
    return duration_info

def takescreenshot(file,screenshotaddress,screenshotnum):
    '''
    para:
        file:视频文件
        duration:视频文件播放时长
        screenshotaddress:存放截图地址，截图后除了新截图其他文件会被清空
        screenshotnum:截图数量
    '''
    logger.info('正在对视频'+file+'截图'+str(screenshotnum)+'张并存入文件夹'+screenshotaddress)
    i=os.path.basename(file)
    if (os.path.isdir(file)) or (i.startswith('.')) or (not(  os.path.splitext(i)[1].lower()== ('.mp4') or os.path.splitext(i)[1].lower()== ('.mkv')  or os.path.splitext(i)[1].lower()== ('.avi') or os.path.splitext(i)[1].lower()== ('.ts')    )):
        logger.error(file+'非视频文件,无法截图')
        raise ValueError (file+'非视频文件,无法截图')
    duration=get_video_duration(file)
    if abs(duration)<1e-9:
        logger.error(file+'视频文件播放时长过短,无法截图')
        raise ValueError (file+'视频文件播放时长过短,无法截图')
    #清空截图文件夹
    ls = os.listdir(screenshotaddress)
    for i in ls:
        c_path = os.path.join(screenshotaddress, i)
        if not (os.path.isdir(c_path)):
            os.remove(c_path)
    timestep=duration*1.0/(screenshotnum+3)
    firststep=timestep*2
    for i in range (screenshotnum):
        firststep=firststep+timestep
        if 'win32' in sys.platform:
            screenshotstr='ffmpeg -ss '+str(firststep)+' -i "'+file+'" -f image2 -y "'+os.path.join(screenshotaddress,str(i+1)+'.jpg')+'"'
        else:
            screenshotstr='ffmpeg -ss '+str(firststep)+' -i "'+file+'" -f image2 -y "'+os.path.join(screenshotaddress,str(i+1)+'.jpg')+'" &> /dev/null'
        #print(screenshotstr)
        os.system(screenshotstr)
    logger.info('截图完毕')

class mediafile(object):
    def __init__(self,mediapath,pathinfo,basic,imgdata):
        self.mediapath         =mediapath
        #如果mediapath是文件夹，就选里面最大的视频文件
        if os.path.isdir(self.mediapath):
            self.isdir=True
            ls = os.listdir(self.mediapath)
            maxsize=0
            for i in ls:
                c_path=os.path.join(self.mediapath, i)
                if (os.path.isdir(c_path)) or (i.startswith('.')) or (not(  os.path.splitext(i)[1].lower()== ('.mp4') or os.path.splitext(i)[1].lower()== ('.mkv')  or os.path.splitext(i)[1].lower()== ('.avi') or os.path.splitext(i)[1].lower()== ('.ts')    )):
                    continue
                filesize=os.path.getsize(c_path)
                if filesize>maxsize:
                    self.address=c_path
                    maxsize=filesize
        else:
            self.address           = mediapath
            self.isdir=False
            
 
        self.pathinfo          = pathinfo

        self.screenshotaddress = basic['screenshot_path']
        self.screenshotnum     = int(basic['picture_num'])
        self.imgdata           = imgdata
        
        self.path              = os.path.dirname(mediapath)
        
        self.type              = pathinfo.type
        self.doubanurl         = pathinfo.doubanurl
        self.imdburl           = pathinfo.imdb_url
        self.bgmurl            = pathinfo.bgm_url
        self.anidburl          = pathinfo.anidb_url
        self.from_url          = pathinfo.from_url
        self.transfer          = pathinfo.transfer
        self.filename          = os.path.basename(self.address)
        self.episodename       = findnum(self.filename)[0]
        self.episode           = int(self.episodename)

        self.sub               = self.pathinfo.sub
        self.englishname       = self.pathinfo.englishname
        self.chinesename       = self.pathinfo.chinesename
 
        if (self.type=='anime' or self.type=='tv'):
            self.season            = self.pathinfo.season
            self.seasonnum         = self.pathinfo.seasonnum
            self.season_ch         = self.pathinfo.season_ch
            self.complete          = self.pathinfo.complete

        self.dlgroup           =['NaN-Raws','NaN Raws','NC-Raws','NC Raws','Lilith-Raws','Lilith Raws','ANi','Skymoon-Raws','Skymoon Raws']
        self.type              ='WEBRip'
        self.Video_Format      ='H264'
        if self.sub in self.dlgroup:
            self.type='WEB-DL'
        self.getscreenshot_done=0
        self.getimgurl_done=0
        self.getmediainfo_done=0
        self.getptgen_done=0
        self.mktorrent_done=0
        self.getinfo_done=0


        self.language=''
        self.country=''
        #根据文件名判断内嵌字幕信息
        self.sublan=''
        jp=0
        sc=0
        tc=0
        if 'SC' in self.filename.upper() or 'CHS' in self.filename.upper() or 'GB' in self.filename.upper() or '简' in self.filename.upper() or '簡' in self.filename.upper():
            sc=1
        if 'TC' in self.filename.upper() or 'CHT' in self.filename.upper() or 'BIG5' in self.filename.upper() or '繁' in self.filename.upper():
            tc=1
        if 'JP' in self.filename.upper() or 'JAPANESE' in self.filename.upper() or '日' in self.filename.upper():
            jp=1
        if jp==0 and sc==0 and tc==1:
            self.sublan='[内嵌繁中]'
        elif jp==0 and sc==1 and tc==0:
            self.sublan='[内嵌简中]'
        elif jp==0 and sc==1 and tc==1:
            self.sublan='[内嵌简繁中字]'
        elif jp==1 and sc==0 and tc==0:
            self.sublan='[内嵌日字]'
        elif jp==1 and sc==0 and tc==1:
            self.sublan='[内嵌繁日双语]'
        elif jp==1 and sc==1 and tc==0:
            self.sublan='[内嵌简日双语]'
        elif jp==1 and sc==1 and tc==1:
            self.sublan='[内嵌简繁日双语]'
        else:
            self.sublan=''
        if jp+sc+tc>0:
            logger.info('根据文件名分析，字幕语言为'+self.sublan)
        else:
            logger.warning('无法根据文件名分析出字幕语言信息')



    def getscreenshot(self):
        if self.getscreenshot_done==0:
            takescreenshot(self.address,self.screenshotaddress,self.screenshotnum)
            self.getscreenshot_done=1
    
    def getimgurl(self,server=''):
        if self.getimgurl_done==1:
            return self.screenshoturl
        self.getscreenshot()
        imgpaths=[]
        for i in range (self.screenshotnum):
            imgpaths.append(os.path.join(self.screenshotaddress,str(i+1)+'.jpg'))
        logger.info('正在将'+self.chinesename +'的第'+self.episodename+'集截图上传'+server+'图床,请稍等...')
        res=img_upload(imgdata=self.imgdata,imglist=imgpaths,host=server,form='bbcode')
        if res=='':
            print(self.chinesename+'上传图床失败,请自行上传图床：')
            temp='\n'
            res=''
            while not temp=='':
                temp=input('')
                res=res+temp+'\n'
        logger.info('成功获得图片链接：\n'+res)
        self.screenshoturl=res
        self.getimgurl_done=1
        return self.screenshoturl

    def dealsubtext(self,res):
        jp=0
        sc=0
        tc=0
        a=res.split('\n\n')
        for item in a:
            if item.startswith('Text'):
                b=item.split('\n')
                for subitem in b:
                    if subitem.lower().startswith('language') or subitem.lower().startswith('title'):
                        if 'SC' in subitem.upper() or 'CHS' in subitem.upper() or 'GB' in subitem.upper() or '简' in subitem.upper() or '簡' in subitem.upper():
                            sc=1
                        if 'TC' in subitem.upper() or 'CHT' in subitem.upper() or 'BIG5' in subitem.upper() or '繁' in subitem.upper():
                            tc=1
                        if 'JP' in subitem.upper() or 'JAPANESE' in subitem.upper() or '日' in subitem.upper():
                            jp=1
        if jp==0 and sc==0 and tc==1:
            self.sublan='[繁体中字]'
        elif jp==0 and sc==1 and tc==0:
            self.sublan='[简体中字]'
        elif jp==0 and sc==1 and tc==1:
            self.sublan='[简繁中字]'
        elif jp==1 and sc==0 and tc==0:
            self.sublan='[日文字幕]'
        elif jp==1 and sc==0 and tc==1:
            self.sublan='[繁日双语]'
        elif jp==1 and sc==1 and tc==0:
            self.sublan='[简日双语]'
        elif jp==1 and sc==1 and tc==1:
            self.sublan='[简繁日双语]'
        if jp+sc+tc>0:
            logger.info('根据mediainfo分析，字幕语言为'+self.sublan)
        else:
            logger.warning('无法根据mediainfo分析出字幕语言信息')

    def dealaudio(self,res):
        ch=0
        jp=0
        en=0
        a=res.split('\n\n')
        for item in a:
            if item.startswith('Audio'):
                b=item.split('\n')
                for subitem in b:
                    if subitem.lower().startswith('language') or subitem.lower().startswith('title'):

                        if 'CHINESE' in subitem.upper() or '中' in subitem.upper() or '国' in subitem.upper():
                            ch=1
                            #logger.info('根据mediainfo音轨分析，语言为'+self.language)
                        if  'JAPANESE' in subitem.upper() or '日' in subitem.upper():
                            jp=1
                            #logger.info('根据mediainfo音轨分析，语言为'+self.language)
                        if 'ENGLISH' in subitem.upper() or '英' in subitem.upper():
                            en=1
                            #logger.info('根据mediainfo音轨分析，语言为'+self.language)


        if jp==0 and ch==0 and en==1:
            self.language='英语'
        elif jp==0 and ch==1 and en==0:
            self.language='国语'
        elif jp==0 and ch==1 and en==1:
            self.language='中英双语'
        elif jp==1 and ch==0 and en==0:
            self.language='日语'
        elif jp==1 and ch==0 and en==1:
            self.language='日英双语'
        elif jp==1 and ch==1 and en==0:
            self.language='中日双语'
        elif jp==1 and ch==1 and en==1:
            self.language='中英日三语'
        else:
            self.language=''

        if jp+ch+en>0:
            logger.info('根据mediainfo音轨分析，语言为'+self.language)
        else:
            logger.warning('无法根据mediainfo分析出音轨语言信息')

    def getmediainfo(self):
        if self.getmediainfo_done==1:
            return self.mediainfo
        a=os.popen("mediainfo \""+self.address+'"')
        #res=a.read()
        res=a.buffer.read().decode('utf-8')
        self.dealsubtext(res)
        self.dealaudio(res)
        ss=res.split('\n')
        ss[1]=':'.join([ss[1].split(':')[0],' '+self.filename])
        self.mediainfo='\n'.join(ss)
        a=os.popen("mediainfo --Output=JSON \""+self.address+'"')
        #res_json=a.read()
        res_json=a.buffer.read().decode('utf-8')
        media_json=json.loads(res_json)
        self.mediainfo_json=media_json
        self.Format            =media_json['media']['track'][0]['Format']
        self.FileSize          =int(media_json['media']['track'][0]['FileSize'].strip())
        self.duration          =float(media_json['media']['track'][0]['Duration'].strip())
        self.Video_Format      =media_json['media']['track'][1]['Format']
        self.Width             =int(media_json['media']['track'][1]['Width'].strip())
        self.Height            =int(media_json['media']['track'][1]['Height'].strip())
        self.BitDepth          =int(media_json['media']['track'][1]['BitDepth'].strip())
        self.Audio_Format      =media_json['media']['track'][2]['Format']
        self.Channels          =int(media_json['media']['track'][2]['Channels'].strip())
        text=self.mediainfo.lower()
        if ('webrip'in text) or ('web-rip' in text):
            self.type='WEBRip'
        if ('webdl'in text) or ('web-dl' in text):
            self.type='WEB-DL'

        if self.Video_Format == 'AVC':
            self.Video_Format = 'H264'
        if self.Video_Format == 'H264' and 'x264' in text:
            self.Video_Format = 'x264'

        if self.Video_Format == 'HEVC':
            self.Video_Format = 'H265'
        if self.Video_Format == 'H265' and 'x265' in text:
            self.Video_Format = 'x265'
        self.getmediainfo_done=1
        return self.mediainfo

    def dealwith_douban_info(self,infolist):
        self.picture=infolist[0].strip()
        for item in infolist:
            if '译\u3000\u3000名'in item:
                self.allName=item[5:].strip().split('/')
                self.small_descr=item[5:].strip()
            if '片\u3000\u3000名'in item:
                self.name=item[5:].strip()
            if '年\u3000\u3000代'in item:
                self.year=item[5:].strip()
                logger.info('根据豆瓣信息分析，年份为'+self.year)
            if '产\u3000\u3000地'in item:
                self.country=item[5:].strip()
                logger.info('根据豆瓣信息分析，地区为'+self.country)
            if '类\u3000\u3000别'in item:
                self.genre=item[5:].strip()
                logger.info('根据豆瓣信息分析，类别为'+self.genre)
            if '语\u3000\u3000言'in item:
                self.language=item[5:].strip()
                logger.info('根据豆瓣信息分析，语言为'+self.language)
            if '上映日期'in item:
                self.release=item[5:].strip()
                logger.info('根据豆瓣信息分析，上映日期为'+self.release)
            if '首\u3000\u3000播'in item:
                self.firstRelease=item[5:].strip()
                logger.info('根据豆瓣信息分析，首播为'+self.firstRelease)
            if '集\u3000\u3000数'in item:
                self.num=int(item[5:].strip())
                if self.pathinfo.max>=self.num:
                    self.complete=1
                logger.info('根据豆瓣信息分析，总集数为'+str(self.num))
            if self.imdburl=='' and 'imdb'in item and '链接'in item and not((item[7:].strip()).endswith('//')):
                self.imdburl=item[7:].strip()
            if '片\u3000\u3000长'in item:
                self.runtime=item[5:].strip()

    def getptgen_douban_info(self):
        if self.getptgen_done==1:
            return
        url='https://api.iyuu.cn/App.Movie.Ptgen?url='+self.doubanurl
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        headers = {
                'user-agent': user_agent,
                'referer': url,
            }
        logger.info('正在获取豆瓣信息')
        try:
            r = requests.get(url,headers=headers,timeout=100)
        except Exception as r:
            logger.error('获取豆瓣信息失败，原因: %s' %(r))
            return 

        logger.info('获取豆瓣信息完毕，正在处理信息，请稍等...')
        
        try:
            info_json=r.json()
            logger.trace(info_json)
        except Exception as r:
            logger.warning('获取豆瓣信息转换json格式失败，原因: %s' %(r))
            return
        
        if not r.ok:
            logger.trace(r.content)
            logger.warning(
                f"获取豆瓣信息失败: HTTP {r.status_code}, reason: {r.reason} ")
            return 

        if 'data' not in info_json or 'format' not in info_json['data']:
            logger.warning(f"豆瓣信息获取失败")
            return 
        
        info=info_json['data']['format']
        self.douban_info=info
        imgurl=re.findall('img[0-9]\.doubanio\.com',self.douban_info)
        if len(imgurl)>0:
            self.douban_info=self.douban_info.replace(imgurl[0],'img9.doubanio.com')
        infolist=info.split('◎')
        self.dealwith_douban_info(infolist)
        self.getptgen_done=1
        


    def getdoubaninfo(self):
        url='https://movieinfo.leaguehd.com/doubanAjax.php?url='+self.doubanurl
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        headers = {
                'user-agent': user_agent,
                'referer': url,
            }
        logger.info('正在获取豆瓣信息，请稍等...')
        try:
            r = requests.get(url,headers=headers,timeout=100)
        except Exception as r:
            logger.warning('通过柠檬获取豆瓣信息失败，原因: %s' %(r))
            return

        logger.info('获取豆瓣信息完毕，正在处理信息，请稍等...')
        try:
            data=r.json()
        except Exception as r:
            logger.warning('通过柠檬获取豆瓣信息转换json格式失败，原因: %s' %(r))
            return

        douban_info=''
        if (data['pic']):
            imgurl=re.findall('img[0-9]\.doubanio\.com',data['pic'])
            douban_info = douban_info+"[img]" + data['pic'].replace(imgurl[0],'img9.doubanio.com') + "[/img]\n"
            #self.picture=data['pic']
        if (data['allName']):
            douban_info = douban_info+ "\n◎译\u3000\u3000名　" + '/'.join(data['allName']);
            self.name=data['allName'][0]
            self.allName='/'.join(data['allName'])
        if (data['name']) :
            douban_info += "\n◎片\u3000\u3000名　" + data['name']
            self.name=data['name']
        if (data['year']):
            douban_info += "\n◎年\u3000\u3000代　" + data['year']
            self.year=data['year']
            logger.info('根据豆瓣信息分析，年份为'+self.year)
        if (data['country'] and len(data['country']) > 0) :
            douban_info += "\n◎产\u3000\u3000地　" + " / ".join(data['country'])
            self.country=" / ".join(data['country'])
            logger.info('根据豆瓣信息分析，地区为'+self.country)
        if (data['genre'] and len(data['genre']) > 0):
            douban_info += "\n◎类\u3000\u3000别　" + " / ".join(data['genre'])
            self.genre=" / ".join(data['genre'])
            logger.info('根据豆瓣信息分析，类别为'+self.genre)
        if (data['language'] and len(data['language']) > 0) :
            douban_info += "\n◎语\u3000\u3000言　" + " / ".join(data['language'])
            self.language=" / ".join(data['language'])
            logger.info('根据豆瓣信息分析，语言为'+self.language)
        if (data['release'] and len(data['release']) > 0) :
            douban_info += "\n◎上映日期　" + " / ".join(data['release'])
            self.release=" / ".join(data['release'])
            logger.info('根据豆瓣信息分析，上映日期为'+self.release)
        if (data['firstRelease'] and len(data['firstRelease']) > 0) :
            douban_info += "\n◎首\u3000\u3000播　" + " / ".join(data['firstRelease'])
            self.firstRelease=" / ".join(data['firstRelease'])
            logger.info('根据豆瓣信息分析，首播为'+self.firstRelease)
        if (data['num']) :
            douban_info += "\n◎集\u3000\u3000数　" + data['num']
            self.media_type='TV_series'
            self.num=int(data['num'])
            if self.pathinfo.max>=self.num:
                self.complete=1
            logger.info('根据豆瓣信息分析，总集数为'+str(self.num))
        if (data['imdbRating']) :
            douban_info += "\n◎IMDb评分  " + data['imdbRating'] + "/10 from " + data['imdbVotes'] + " users"
        if (data['imdbUrl']) :
            douban_info += "\n◎IMDb链接  " + data['imdbUrl']
            self.imdburl=data['imdbUrl']
            pathinfo.imdb_url=data['imdbUrl']
            logger.info('根据豆瓣信息分析，imdb链接为'+data['imdbUrl'])
        if (data['rating']) :
            douban_info += "\n◎豆瓣评分　" + data['rating'] + "/10 from " + data['votes'] + " users";
        if (data['url']) :
            douban_info += "\n◎豆瓣链接　" + data['url']
        if (data['runtime'] and len(data['runtime']) > 0) :
            douban_info += "\n◎片　　长　" + " / ".join(data['runtime'])

        if (data['director'] and len(data['director']) > 0) :
            for i in range (len(data['director'])):
                if i==0:
                    douban_info += "\n◎导　　演　" + (data['director'][i]['name'])
                else:
                    douban_info += "\n　　　　　  " + (data['director'][i]['name'])

        if (data['writer'] and len(data['writer']) > 0) :
            for i in range (len(data['writer'])):
                if i==0:
                    douban_info += "\n◎编　　剧　" + (data['writer'][i]['name'])
                else:
                    douban_info += "\n　　　　　  " + (data['writer'][i]['name'])

        if (data['cast'] and len(data['cast']) > 0) :
            for i in range (len(data['cast'])):
                if i==0:
                    douban_info += "\n◎主　　演　" + (data['cast'][i]['name'])
                else:
                    douban_info += "\n　　　　　  " + (data['cast'][i]['name'])

        if (data['tags'] and len(data['tags']) > 0) :
            douban_info += "\n\n\n◎标　　签　" + " | ".join(data['tags'])
        if (data['plot']) :
            douban_info += "\n\n◎简　　介　" + "\n\n " +(data['plot'].replace('<br \\/>', "\n").replace('<wbr \\/>', "\n"))

        if (data['awards'] and len(data['awards']) > 0) :
            awardstr=''
            for item in data['awards']:
                awardstr=awardstr+"\n\n　　" + item['title'];
                for itemc in item['content']:
                    awardstr=awardstr+"\n　　" + itemc
            douban_info += "\n\n◎获奖情况　" + awardstr

        douban_info =douban_info+ "\n\n"
        self.douban_info=douban_info
        self.getptgen_done=1

    def mktorrent(self,tracker='https://announce.leaguehd.com/announce.php'):
        if self.mktorrent_done==1:
            return
        torrentpath=os.path.join(self.screenshotaddress,str(self.episode)+'.torrent')
        self.torrentpath=torrentpath
        mktorrent(self.mediapath,torrentpath,tracker=tracker)
        self.mktorrent_done=1

    def movefile(self):
        path=os.path.dirname(self.address)
        new_path=os.path.join(os.path.dirname(path),'temp')
        os.rename(path,new_path)
        os.mkdir(path)
        shutil.move(os.path.join(new_path,self.filename), path)

    def getfullinfo(self,tracker='https://announce.leaguehd.com/announce.php'):
        if self.getinfo_done==1:
            return

        while not self.getptgen_done==1:
            self.getptgen_douban_info()
            if self.getptgen_done<1:
                self.getdoubaninfo()
            if self.getptgen_done<1:
                time.sleep(3)


        self.getmediainfo()
        self.uploadname=self.englishname+' '+str(self.year)
        self.small_descr=self.chinesename

        if self.pathinfo.type=='anime' or self.pathinfo.type=='tv':
            self.uploadname=self.uploadname+' '+self.season
            self.small_descr=self.small_descr+' ('+self.season_ch+') '
            if not self.isdir:
                self.uploadname=self.uploadname+'E'+self.episodename
                self.small_descr=self.small_descr+'(第'+self.episodename+'集) '
            elif self.complete==1:
                self.uploadname=self.uploadname
                self.small_descr=self.small_descr+'(全'+str(self.pathinfo.max)+'集)'
            else:
                self.uploadname=self.uploadname+'E'+str(self.pathinfo.min).zfill(2)+'-E'+str(self.pathinfo.max).zfill(2)
                self.small_descr=self.small_descr+'(第'+str(self.pathinfo.min).zfill(2)+'-'+str(self.pathinfo.max).zfill(2)+'集)'




        self.uploadname_ssd=self.uploadname+' '+self.type+' '+str(self.Height)+'p '+self.Video_Format+' '+self.Audio_Format+'-'+self.sub
        self.uploadname    =self.uploadname+' '+str(self.Height)+'p '+self.type+' '+self.Video_Format+' '+self.Audio_Format+'-'+self.sub
        
        try:
            if not self.language=='':
                self.small_descr=self.small_descr+'['+self.language+'] '
        except:
            logger.warning('未找到资源语言信息，默认为日语')
            self.small_descr=self.small_descr+'[日语] '

        if not self.sublan=='':
            self.small_descr=self.small_descr+self.sublan
        self.small_descr=self.small_descr.replace('（','(').replace('）',')')


        self.getimgurl()
        self.content=self.douban_info+"\n[quote=Mediainfo]\n"+self.mediainfo+"[/quote]\n"+self.screenshoturl
        self.mktorrent(tracker)
        self.getinfo_done=1

    def print(self):
        self.getfullinfo()
        attr=['uploadname','small_descr','content']
        for item in attr:
            exec('print("'+item+':"  ,self.'+item+'  )')


