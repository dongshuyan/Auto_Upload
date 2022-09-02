from loguru import logger
import time
import os
from selenium.webdriver.common.keys import Keys
from auto_upload.utils.uploader.upload_tools import *
from selenium.webdriver.support.select import Select
import re
from selenium.webdriver.common.by import By

def lemonhd_upload(web,file1,record_path,qbinfo,basic):
    if 'anime' in file1.pathinfo.type.lower():
        return lemonhd_upload_anime(web,file1,record_path,qbinfo,basic)
    elif 'tv' in file1.pathinfo.type.lower():
        return lemonhd_upload_tv(web,file1,record_path,qbinfo,basic)
    elif 'movie' in file1.pathinfo.type.lower():
        return lemonhd_upload_tv(web,file1,record_path,qbinfo,basic)

def lemon_check(web):
    logger.info('正在自动审核')
    #自动审核
    try:
        checkbox=web.driver.find_elements(By.NAME,'check_type')[0]
        if not checkbox.is_selected():
            checkbox.click()
        logger.info('自动选择审核通过')
        time.sleep(2)
        web.driver.find_elements(By.ID,'qr')[0].click()
        logger.info('已审核')
        return True
    except Exception as r:
        logger.info('审核失败')
        return False

def lemonhd_upload_anime(web,file1,record_path,qbinfo,basic):

    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+web.site.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+web.site.sitename

    try:
        web.driver.get(web.site.uploadurl)
    except Exception as r:
        logger.warning('打开发布页面发生错误，错误信息: %s' %(r))
        return False,fileinfo+'打开发布页面发生错误'
        
    logger.info('正在'+web.site.sitename+'发布种子...')
    try:
        web.driver.find_element(By.CLASS_NAME,'file').send_keys(file1.torrentpath);
    except Exception as r:
        logger.warning('上传种子文件发生错误，错误信息: %s' %(r))
        return False,fileinfo+'上传种子文件发生错误'
    logger.info('已成功上传种子')
    
    try:
        if len(web.driver.find_elements(By.NAME,'name'))<=0:
            web.driver.execute_script("window.scrollBy(0,300)")
    except Exception as r:
        logger.warning('下拉页面发生错误，错误信息: %s' %(r))
        return False,fileinfo+'下拉页面发生错误'

    #web.driver.find_elements(By.NAME,'small_descr')[0].click()
    try:
        web.driver.find_elements(By.NAME,'small_descr')[0].send_keys(file1.small_descr+file1.pathinfo.exinfo)
    except Exception as r:
        logger.warning('填写副标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写副标题发生错误'
    logger.info('已成功填写副标题')
    
    #web.driver.find_elements(By.NAME,'douban_url')[0].click()
    try:
        web.driver.find_elements(By.NAME,'douban_url')[0].send_keys(file1.doubanurl)
    except Exception as r:
        logger.warning('填写豆瓣链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写豆瓣链接发生错误'
    logger.info('已成功填写豆瓣链接')
    
    #web.driver.find_elements(By.NAME,'url')[0].click()
    try:
        web.driver.find_elements(By.NAME,'url')[0].send_keys(file1.imdburl)
    except Exception as r:
        logger.warning('填写IMDb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写IMDb链接发生错误'
    logger.info('已成功填写IMDb链接')
    
    #web.driver.find_elements(By.NAME,'bangumi_url')[0].click()
    try:
        web.driver.find_elements(By.NAME,'bangumi_url')[0].send_keys(file1.bgmurl)
    except Exception as r:
        logger.warning('填写Bangumi链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写Bangumi链接发生错误'
    logger.info('已成功填写Bangumi链接')
    
    #web.driver.find_elements(By.NAME,'anidb_url')[0].click()
    try:
        web.driver.find_elements(By.NAME,'anidb_url')[0].send_keys(file1.anidburl)
    except Exception as r:
        logger.warning('填写Anidb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写Anidb链接发生错误'
    logger.info('已成功填写Anidb链接')
    
    #web.driver.find_elements(By.NAME,'cn_name')[0].click()
    try:
        web.driver.find_elements(By.NAME,'cn_name')[0].send_keys(file1.chinesename)
    except Exception as r:
        logger.warning('填写中文名发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写中文名发生错误'
    logger.info('已成功填写中文名')
    
    #web.driver.find_elements(By.NAME,'en_name')[0].click()
    try:
        web.driver.find_elements(By.NAME,'en_name')[0].send_keys(file1.englishname)
    except Exception as r:
        logger.warning('填写英文名发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写英文名发生错误'
    logger.info('已成功填写英文名')
    
    logger.info('正在填写简介,请稍等...')
    #web.driver.find_elements(By.NAME,'descr')[0].click()
    try:
        if 'league' in file1.sub.lower():
            web.driver.find_elements(By.NAME,'descr')[0].send_keys(file1.douban_info+'\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-info-s3.png[/img]\n[quote=Mediainfo]\n'+file1.mediainfo+'\n[/quote]\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-screen-s3.png[/img]\n'+file1.screenshoturl)
        else:
            web.driver.find_elements(By.NAME,'descr')[0].send_keys(file1.content)
    except Exception as r:
        logger.warning('填写简介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写简介发生错误'
    logger.info('已成功填写简介')
    
    #web.driver.find_elements(By.NAME,'year')[0].click()
    try:
        web.driver.find_elements(By.NAME,'year')[0].send_keys(str(file1.year))
    except Exception as r:
        logger.warning('填写年份发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写年份发生错误'
    logger.info('已成功填写年份',str(file1.year))

    try:
        if 'movie' in file1.pathinfo.type.lower():
            select_animate_type = web.driver.find_element('name','animate_type')  
            select_animate_type_ob = Select(select_animate_type)   
            select_animate_type_ob.select_by_value('1')
            logger.info('已成功选择类型为movie')
            select_animate_type = web.driver.find_element('name','edition_sel')  
            select_animate_type_ob = Select(select_animate_type)   
            select_animate_type_ob.select_by_value('1')
            logger.info('已成功选择类型为原版/普通版')
        else:
            if file1.pathinfo.collection==0:
                select_animate_type = web.driver.find_element('name','animate_type')  
                select_animate_type_ob = Select(select_animate_type)   
                select_animate_type_ob.select_by_value('3')
                logger.info('已成功选择类型为TV')  
            else:
                select_animate_type = web.driver.find_element('name','animate_type')  
                select_animate_type_ob = Select(select_animate_type)   
                select_animate_type_ob.select_by_value('6')
                logger.info('已成功选择类型为collection')

            if file1.pathinfo.complete==0:
                is_complete_checkbox=web.driver.find_elements(By.NAME,'is_complete')[0]
                if not is_complete_checkbox.is_selected():
                    is_complete_checkbox.click()
                logger.info('已成功选择未完结')

            if file1.pathinfo.collection==0:
                #web.driver.find_elements(By.NAME,'series')[0].click()
                web.driver.find_elements(By.NAME,'series')[0].send_keys('第'+file1.episodename+'话')
            elif file1.pathinfo.complete==1:
                web.driver.find_elements(By.NAME,'series')[0].send_keys('TV '+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2)+' Fin')
            else:
                web.driver.find_elements(By.NAME,'series')[0].send_keys('TV '+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2))
            logger.info('已成功填写集数')

    except Exception as r:
        logger.warning('选择类型发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择类型发生错误'



    

    try:
        select_team_sel = web.driver.find_element('name','team_sel')   
        select_team_sel_ob = Select(select_team_sel)      
        if 'i18n' in file1.sub.lower():
            select_team_sel_ob.select_by_value('9')
        elif 'lhd' in file1.sub.lower():
            select_team_sel_ob.select_by_value('14')
        elif 'leaguehd' in file1.sub.lower():
            select_team_sel_ob.select_by_value('8')
        elif 'leaguenf' in file1.sub.lower():
            select_team_sel_ob.select_by_value('12')
        elif 'leaguetv' in file1.sub.lower():
            select_team_sel_ob.select_by_value('10')
        elif 'leaguecd' in file1.sub.lower():
            select_team_sel_ob.select_by_value('11')
        elif 'leagueweb' in file1.sub.lower():
            select_team_sel_ob.select_by_value('13')
        elif 'cint' in file1.sub.lower():
            select_team_sel_ob.select_by_value('15')
        else:
            web.driver.find_elements(By.NAME,'source_author')[0].send_keys(file1.sub)
    except Exception as r:
        logger.warning('填写制作组发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写制作组发生错误'
    logger.info('已成功填写制作组')



    #选择媒介
    try:
        select_sel = web.driver.find_element('name','animate_category')    
        select_sel_ob = Select(select_sel)    
        if file1.type=='WEB-DL':
            select_sel_ob.select_by_value('7')
        elif 'bdrip' in file1.type.lower() :
            select_sel_ob.select_by_value('2')
        elif 'hdtvrip' in file1.type.lower() :
            select_sel_ob.select_by_value('6')
        elif 'hdtv' in file1.type.lower():
            select_sel_ob.select_by_value('5')
        elif 'remux' in file1.type.lower():
            select_sel_ob.select_by_value('10')
        elif 'dvdrip' in file1.type.lower() :
            select_sel_ob.select_by_value('4')
        else:
            select_sel_ob.select_by_value('7')
        logger.info('已成功选择质量为'+file1.type)
    except Exception as r:
        logger.warning('选择媒介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择媒介发生错误'
    logger.info('已成功填写媒介为'+file1.type)


    #选择编码
    try:
        select_codec_sel = web.driver.find_element('name','codec_sel') 
        select_codec_sel_ob = Select(select_codec_sel) 
        if file1.Video_Format=='H264':
            select_codec_sel_ob.select_by_value('1')
        elif file1.Video_Format=='x264':
            select_codec_sel_ob.select_by_value('12')
        elif file1.Video_Format=='H265':
            select_codec_sel_ob.select_by_value('10')
        elif file1.Video_Format=='x265':
            select_codec_sel_ob.select_by_value('11')
        else:
            select_codec_sel_ob.select_by_value('1')
        logger.info('已成功选择编码为'+file1.Video_Format)
    except Exception as r:
        logger.warning('选择编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择编码发生错误'
    logger.info('已成功填写编码为'+file1.Video_Format)

    #选择音频编码
    try:
        select_source_sel = web.driver.find_element('name','audiocodec_sel')   
        select_source_sel_ob = Select(select_source_sel)    
        if file1.Audio_Format.upper()=='AAC':
            select_source_sel_ob.select_by_value('8')
        elif 'DTS-HD HR' in file1.Audio_Format.upper() or 'DTS-HDHR' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('104')
        elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('5')
        elif 'TrueHD Atmos' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('1')
        elif 'LPCM' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('15')
        elif 'TrueHD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'FLAC' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('7')
        elif 'APE' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('11')
        elif 'MP3' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('9')
        elif 'OGG' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('10')
        elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('14')
        elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('4')
        elif 'DTS' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('6')
        elif 'WAV' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('12')
        elif 'M4A' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('13')
        else:
            select_source_sel_ob.select_by_value('8')
    except Exception as r:
        logger.warning('选择音频编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择音频编码发生错误'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    try:
        select_team_sel = web.driver.find_element('name','standard_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if '8K' in file1.standard_sel:
            select_team_sel_ob.select_by_value('6')
        elif '2160' in file1.standard_sel:
            select_team_sel_ob.select_by_value('1')
        elif '1080p' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '1080i' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '720' in file1.standard_sel:
            select_team_sel_ob.select_by_value('4')
        elif '480' in file1.standard_sel:
            select_team_sel_ob.select_by_value('5')
        else:
            select_team_sel_ob.select_by_value('2')
    except Exception as r:
        logger.warning('选择分辨率发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择分辨率发生错误'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    

    #选择地区
    try:
        select_team_sel = web.driver.find_element('name','processing_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if not file1.country=='':
            if '大陆' in file1.country:
                select_team_sel_ob.select_by_value('1')
                logger.info('国家信息已选择'+file1.country)
            elif '香港' in file1.country:
                select_team_sel_ob.select_by_value('2')
                logger.info('国家信息已选择'+file1.country)
            elif '台湾' in file1.country:
                select_team_sel_ob.select_by_value('2')
                logger.info('国家信息已选择'+file1.country)
            elif '美国' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '英国' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '法国' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '韩国' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '日本' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '印度' in file1.country:
                select_team_sel_ob.select_by_value('5')
                logger.info('国家信息已选择'+file1.country)
            else:
                select_team_sel_ob.select_by_value('5')
                logger.info('未找到资源国家信息，已默认其他')
        else:
            select_team_sel_ob.select_by_value('4')
            logger.info('未找到资源国家信息，已默认日本')
    except Exception as r:
        logger.warning('选择地区发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择地区发生错误'
    logger.info('已成功选择分辨率为'+file1.country)

    #选择来源
    try:
        select_original = web.driver.find_element('name','original')    
        select_original_ob = Select(select_original)
        if file1.pathinfo.transfer==1:
            select_original_ob.select_by_value('1')
            logger.info('已选择来源为转载')
            web.driver.find_elements(By.NAME,'from_url')[0].send_keys(file1.from_url)
            logger.info('已成功填写转载地址')
        elif file1.pathinfo.transfer==0:
            select_original_ob.select_by_value('2')
            logger.info('已选择来源为原创')
        else:
            select_original_ob.select_by_value('1')
            logger.info('已默认来源为转载')
            web.driver.find_elements(By.NAME,'from_url')[0].send_keys(file1.from_url)
            logger.info('已成功填写转载地址')
    except Exception as r:
        logger.warning('选择来源发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择来源发生错误'
    logger.info('成功选择来源')

    
    try:
        if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
            checkbox=web.driver.find_elements(By.NAME,'tag_zz')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择中字')
    except Exception as r:
        logger.warning('选择中字发生错误，错误信息: %s' %(r))


    try:
        if '国' in file1.language or '中' in file1.language:
            checkbox=web.driver.find_elements(By.NAME,'tag_gy')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择国语')
    except Exception as r:
        logger.warning('选择国语发生错误，错误信息: %s' %(r))

    try:
        if 'lemonhd' in file1.pathinfo.exclusive and ('league' in file1.sub.lower() or 'lhd' in file1.sub.lower() or 'cint' in file1.sub.lower() or 'i18n' in file1.sub.lower() ):
            checkbox=web.driver.find_elements(By.NAME,'tag_jz')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择禁转')
    except Exception as r:
        logger.warning('选择禁转错误，错误信息: %s' %(r))


    try:
        if web.site.uplver==1:
            checkbox=web.driver.find_elements(By.NAME,'uplver')[0]
            if not checkbox.is_selected():
                checkbox.click()
            logger.info('已选择匿名发布')
    except Exception as r:
        logger.warning('选择匿名发布发生错误，错误信息: %s' %(r))

    #a=input('check')
    String_url = web.driver.current_url;
    web.driver.find_elements(By.ID,'qr')[0].click()
    logger.info('已发布成功')

    String_url =finduploadurl(web.driver)

    downloadurl=finddownloadurl(driver=web.driver,elementstr='/html/body/table[2]/tbody/tr[2]/td/table[1]/tbody/tr[10]/td[2]/a[2]')
    
    if downloadurl=='已存在':
        return True,fileinfo+'种子发布失败,失败原因:种子'+downloadurl+',当前网址:'+web.driver.current_url

    recordupload(os.path.join(record_path,web.site.sitename+'_torrent.csv'),file1,String_url,downloadurl)

    if not downloadurl =='':

        res=qbseed(url=downloadurl,filepath=file1.downloadpath,qbinfo=qbinfo,category=file1.pathinfo.category)
        if res:
            logger.info(fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url)
        else:
            logger.warning(fileinfo+'添加种子失败,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url)
            return True,fileinfo+'种子发布成功,但是添加种子失败,请手动添加种子，种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
    else:
        logger.warning(fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url)
        return False,fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url
    
    if 'check' in dir(web.site) and web.site.check==False:
        return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url

    res=lemon_check(web)
    if res:
        logger.info('成功审核第'+file1.episodename+'集的资源')
        infostr=fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url+'且成功审核第'+file1.episodename+'集的资源'
        logger.info(infostr)
        return True,infostr
    else:
        logger.info('未成功审核第'+file1.episodename+'集的资源')
        return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url+'但未成功审核第'+file1.episodename+'集的资源'
    


def lemonhd_upload_tv(web,file1,record_path,qbinfo,basic):

    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+web.site.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+web.site.sitename

    try:
        web.driver.get('https://lemonhd.org/upload_tv.php')
    except Exception as r:
        logger.warning('打开发布页面发生错误，错误信息: %s' %(r))
        return False,fileinfo+'打开发布页面发生错误'
        
    logger.info('正在'+web.site.sitename+'发布种子...')
    try:
        web.driver.find_element(By.CLASS_NAME,'file').send_keys(file1.torrentpath);
    except Exception as r:
        logger.warning('上传种子文件发生错误，错误信息: %s' %(r))
        return False,fileinfo+'上传种子文件发生错误'
    logger.info('已成功上传种子')
    
    try:
        if len(web.driver.find_elements(By.NAME,'name'))<=0:
            web.driver.execute_script("window.scrollBy(0,300)")
    except Exception as r:
        logger.warning('下拉页面发生错误，错误信息: %s' %(r))
        return False,fileinfo+'下拉页面发生错误'

    try:
        if len(web.driver.find_elements(By.NAME,'name'))<=0:
            web.driver.execute_script("window.scrollBy(0,300)")
        #web.driver.find_elements(By.NAME,'name')[0].click()
        web.driver.find_elements(By.NAME,'name')[0].send_keys(Keys.CONTROL, "a")
        web.driver.find_elements(By.NAME,'name')[0].send_keys(Keys.BACKSPACE)
        web.driver.find_elements(By.NAME,'name')[0].send_keys(Keys.BACKSPACE)
        web.driver.find_elements(By.NAME,'name')[0].send_keys(file1.uploadname)
        logger.info('已成功填写主标题')
    except Exception as r:
        logger.warning('填写主标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写主标题发生错误'

    try:
        #web.driver.find_elements(By.NAME,'small_descr')[0].click()
        web.driver.find_elements(By.NAME,'small_descr')[0].send_keys(file1.small_descr+file1.pathinfo.exinfo)
        logger.info('已成功填写副标题')
    except Exception as r:
        logger.warning('填写副标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写副标题发生错误'
    
    #web.driver.find_elements(By.NAME,'douban_url')[0].click()
    try:
        web.driver.find_elements(By.NAME,'douban_url')[0].send_keys(file1.doubanurl)
    except Exception as r:
        logger.warning('填写豆瓣链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写豆瓣链接发生错误'
    logger.info('已成功填写豆瓣链接')
    
    #web.driver.find_elements(By.NAME,'url')[0].click()
    try:
        web.driver.find_elements(By.NAME,'url')[0].send_keys(file1.imdburl)
    except Exception as r:
        logger.warning('填写IMDb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写IMDb链接发生错误'
    logger.info('已成功填写IMDb链接')

    try:
        if 'league' in file1.sub.lower():
            web.driver.find_elements(By.NAME,'descr')[0].send_keys(file1.douban_info+'\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-info-s3.png[/img]\n[quote=Mediainfo]\n'+file1.mediainfo+'\n[/quote]\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-screen-s3.png[/img]\n'+file1.screenshoturl)
        else:
            web.driver.find_elements(By.NAME,'descr')[0].send_keys(file1.content)
    except Exception as r:
        logger.warning('填写简介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写简介发生错误'
    logger.info('已成功填写简介')

    try:
        if 'show' in file1.pathinfo.type.lower():
            select_animate_type = web.driver.find_element('name','type')  
            select_animate_type_ob = Select(select_animate_type)   
            select_animate_type_ob.select_by_value('403')
            logger.info('已成功选择类型为TV Shows(综艺)')
        else:
            select_animate_type = web.driver.find_element('name','type')  
            select_animate_type_ob = Select(select_animate_type)   
            select_animate_type_ob.select_by_value('402')
            logger.info('已成功选择类型为TV Series(电视剧)')

        if file1.pathinfo.complete==1:
            is_complete_checkbox=web.driver.find_elements(By.NAME,'is_complete')[0]
            if not is_complete_checkbox.is_selected():
                is_complete_checkbox.click()
            logger.info('已成功选择已完结')

        web.driver.find_elements(By.NAME,'t_season')[0].send_keys(file1.season)

        if file1.pathinfo.collection==0:
            #web.driver.find_elements(By.NAME,'series')[0].click()
            web.driver.find_elements(By.NAME,'series')[0].send_keys('E'+file1.episodename)
        elif file1.pathinfo.complete==1:
            web.driver.find_elements(By.NAME,'series')[0].send_keys('E'+str(file1.pathinfo.min).zfill(2)+'-E'+str(file1.pathinfo.max).zfill(2)+' Fin')
        else:
            web.driver.find_elements(By.NAME,'series')[0].send_keys('E'+str(file1.pathinfo.min).zfill(2)+'-E'+str(file1.pathinfo.max).zfill(2))
        logger.info('已成功填写集数')

    except Exception as r:
        logger.warning('选择类型发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择类型发生错误'



    try:
        select_team_sel = web.driver.find_element('name','edition_sel')   
        select_team_sel_ob = Select(select_team_sel)      
        select_team_sel_ob.select_by_value('1')
    except Exception as r:
        logger.warning('填写制作组发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写制作组发生错误'
    logger.info('版本已选择原版')

    try:
        select_team_sel = web.driver.find_element('name','team_sel')   
        select_team_sel_ob = Select(select_team_sel)      
        if 'i18n' in file1.sub.lower():
            select_team_sel_ob.select_by_value('9')
        elif 'lhd' in file1.sub.lower():
            select_team_sel_ob.select_by_value('14')
        elif 'leaguehd' in file1.sub.lower():
            select_team_sel_ob.select_by_value('8')
        elif 'leaguenf' in file1.sub.lower():
            select_team_sel_ob.select_by_value('12')
        elif 'leaguetv' in file1.sub.lower():
            select_team_sel_ob.select_by_value('10')
        elif 'leaguecd' in file1.sub.lower():
            select_team_sel_ob.select_by_value('11')
        elif 'leagueweb' in file1.sub.lower():
            select_team_sel_ob.select_by_value('13')
        elif 'cint' in file1.sub.lower():
            select_team_sel_ob.select_by_value('15')
        else:
            logger.info('非官组资源')
    except Exception as r:
        logger.warning('填写制作组发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写制作组发生错误'
    logger.info('已成功填写制作组')



    #选择媒介
    try:
        select_sel = web.driver.find_element('name','medium_sel')    
        select_sel_ob = Select(select_sel)    
        if file1.type=='WEB-DL':
            select_sel_ob.select_by_value('11')
        elif 'rip' in file1.type.lower() :
            select_sel_ob.select_by_value('7')
        elif 'hdtvrip' in file1.type.lower() :
            select_sel_ob.select_by_value('7')
        elif 'hdtv' in file1.type.lower():
            select_sel_ob.select_by_value('5')
        elif 'remux' in file1.type.lower():
            select_sel_ob.select_by_value('3')
        elif 'dvd' in file1.type.lower() :
            select_sel_ob.select_by_value('6')
        else:
            select_sel_ob.select_by_value('7')
        logger.info('已成功选择质量为'+file1.type)
    except Exception as r:
        logger.warning('选择媒介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择媒介发生错误'
    logger.info('已成功填写媒介为'+file1.type)


    #选择编码
    try:
        select_codec_sel = web.driver.find_element('name','codec_sel') 
        select_codec_sel_ob = Select(select_codec_sel) 
        if file1.Video_Format=='H264':
            select_codec_sel_ob.select_by_value('1')
        elif file1.Video_Format=='x264':
            select_codec_sel_ob.select_by_value('12')
        elif file1.Video_Format=='H265':
            select_codec_sel_ob.select_by_value('10')
        elif file1.Video_Format=='x265':
            select_codec_sel_ob.select_by_value('11')
        else:
            select_codec_sel_ob.select_by_value('1')
        logger.info('已成功选择编码为'+file1.Video_Format)
    except Exception as r:
        logger.warning('选择编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择编码发生错误'
    logger.info('已成功填写编码为'+file1.Video_Format)

    #选择音频编码
    try:
        select_source_sel = web.driver.find_element('name','audiocodec_sel')   
        select_source_sel_ob = Select(select_source_sel)    
        if file1.Audio_Format.upper()=='AAC':
            select_source_sel_ob.select_by_value('8')
        elif 'DTS-HD HR' in file1.Audio_Format.upper() or 'DTS-HDHR' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('104')
        elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('5')
        elif 'TrueHD Atmos' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('1')
        elif 'LPCM' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('15')
        elif 'TrueHD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'FLAC' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('7')
        elif 'APE' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('11')
        elif 'MP3' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('9')
        elif 'OGG' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('10')
        elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('14')
        elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('4')
        elif 'DTS' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('6')
        elif 'WAV' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('12')
        elif 'M4A' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('13')
        else:
            select_source_sel_ob.select_by_value('8')
    except Exception as r:
        logger.warning('选择音频编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择音频编码发生错误'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    try:
        select_team_sel = web.driver.find_element('name','standard_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if '8K' in file1.standard_sel:
            select_team_sel_ob.select_by_value('6')
        elif '2160' in file1.standard_sel:
            select_team_sel_ob.select_by_value('1')
        elif '1080p' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '1080i' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '720' in file1.standard_sel:
            select_team_sel_ob.select_by_value('4')
        elif '480' in file1.standard_sel:
            select_team_sel_ob.select_by_value('5')
        else:
            select_team_sel_ob.select_by_value('2')
    except Exception as r:
        logger.warning('选择分辨率发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择分辨率发生错误'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    

    #选择地区
    try:
        select_team_sel = web.driver.find_element('name','processing_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if not file1.country=='':
            if '大陆' in file1.country:
                select_team_sel_ob.select_by_value('1')
                logger.info('国家信息已选择'+file1.country)
            elif '香港' in file1.country:
                select_team_sel_ob.select_by_value('2')
                logger.info('国家信息已选择'+file1.country)
            elif '台湾' in file1.country:
                select_team_sel_ob.select_by_value('2')
                logger.info('国家信息已选择'+file1.country)
            elif '美国' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '英国' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '法国' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '韩国' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '日本' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '印度' in file1.country:
                select_team_sel_ob.select_by_value('5')
                logger.info('国家信息已选择'+file1.country)
            else:
                select_team_sel_ob.select_by_value('5')
                logger.info('未找到资源国家信息，已默认其他')
        else:
            select_team_sel_ob.select_by_value('4')
            logger.info('未找到资源国家信息，已默认日本')
    except Exception as r:
        logger.warning('选择地区发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择地区发生错误'
    logger.info('已成功选择分辨率为'+file1.country)

    
    try:
        if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
            checkbox=web.driver.find_elements(By.NAME,'tag_zz')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择中字')
    except Exception as r:
        logger.warning('选择中字发生错误，错误信息: %s' %(r))


    try:
        if '国' in file1.language or '中' in file1.language:
            checkbox=web.driver.find_elements(By.NAME,'tag_gy')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择国语')
    except Exception as r:
        logger.warning('选择国语发生错误，错误信息: %s' %(r))

    try:
        if 'lemonhd' in file1.pathinfo.exclusive and ('league' in file1.sub.lower() or 'lhd' in file1.sub.lower() or 'cint' in file1.sub.lower() or 'i18n' in file1.sub.lower() ):
            checkbox=web.driver.find_elements(By.NAME,'tag_jz')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择禁转')
    except Exception as r:
        logger.warning('选择禁转错误，错误信息: %s' %(r))

        
    try:
        if web.site.uplver==1:
            checkbox=web.driver.find_elements(By.NAME,'uplver')[0]
            if not checkbox.is_selected():
                checkbox.click()
            logger.info('已选择匿名发布')
    except Exception as r:
        logger.warning('选择匿名发布发生错误，错误信息: %s' %(r))

    #a=input('check')
    String_url = web.driver.current_url;
    web.driver.find_elements(By.ID,'qr')[0].click()
    logger.info('已发布成功')

    String_url =finduploadurl(web.driver)

    downloadurl=finddownloadurl(driver=web.driver,elementstr='/html/body/table[2]/tbody/tr[2]/td/table[1]/tbody/tr[10]/td[2]/a[2]')
    
    if not 'https=1&' in downloadurl:
        downloadurl_temp=downloadurl.split('.php?')
        downloadurl=downloadurl_temp[0]+'.php?https=1&'+downloadurl_temp[1]
        del(downloadurl_temp)
    
    if downloadurl=='已存在':
        return True,fileinfo+'种子发布失败,失败原因:种子'+downloadurl+',当前网址:'+web.driver.current_url

    recordupload(os.path.join(record_path,web.site.sitename+'_torrent.csv'),file1,String_url,downloadurl)

    if not downloadurl =='':

        #res=qbseed(url=downloadurl,filepath=file1.downloadpath,qbinfo=qbinfo)
        res=qbseed(url=downloadurl,filepath=file1.downloadpath,qbinfo=qbinfo,category=file1.pathinfo.category)
        if res:
            logger.info(fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url)
        else:
            logger.warning(fileinfo+'添加种子失败,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url)
            return True,fileinfo+'种子发布成功,但是添加种子失败,请手动添加种子，种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
    else:
        logger.warning(fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url)
        return False,fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url
    
    
    #return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
    
    if 'check' in dir(web.site) and web.site.check==False:
        return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url

    res=lemon_check(web)

    if res:
        logger.info('成功审核第'+file1.episodename+'集的资源')
        infostr=fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url+'且成功审核第'+file1.episodename+'集的资源'
        logger.info(infostr)
        return True,infostr
    else:
        logger.info('未成功审核第'+file1.episodename+'集的资源')
        return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url+'但未成功审核第'+file1.episodename+'集的资源'
    


    
