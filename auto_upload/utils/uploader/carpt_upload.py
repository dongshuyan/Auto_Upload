from loguru import logger
import time
import os
from selenium.webdriver.common.keys import Keys
from auto_upload.utils.uploader.upload_tools import *
from selenium.webdriver.support.select import Select
import re
from selenium.webdriver.common.by import By

def carpt_upload(web,file1,record_path,qbinfo,basic):

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
        #web.driver.find_elements(By.NAME,'name')[0].click()
        web.driver.find_elements(By.NAME,'name')[0].send_keys(Keys.CONTROL, "a")
        web.driver.find_elements(By.NAME,'name')[0].send_keys(Keys.BACKSPACE)
        web.driver.find_elements(By.NAME,'name')[0].send_keys(Keys.BACKSPACE)
        web.driver.find_elements(By.NAME,'name')[0].send_keys(file1.uploadname)
        logger.info('已成功填写主标题')
    except Exception as r:
        logger.warning('填写主标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写主标题发生错误'
    logger.info('已成功填写主标题')

    try:
        #web.driver.find_elements(By.NAME,'small_descr')[0].click()
        web.driver.find_elements(By.NAME,'small_descr')[0].send_keys(file1.small_descr+file1.pathinfo.exinfo)
        logger.info('已成功填写副标题')
    except Exception as r:
        logger.warning('填写副标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写副标题发生错误'
    logger.info('已成功填写副标题')

    try:
        #web.driver.find_elements(By.NAME,'url')[0].click()
        web.driver.find_elements(By.NAME,'url')[0].send_keys(file1.imdburl)
        logger.info('已成功填写IMDb链接')
    except Exception as r:
        logger.warning('填写IMDb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写IMDb链接发生错误'
    logger.info('已成功填写IMDb链接')


    logger.info('正在填写简介,请稍等...')
    try:
        #web.driver.find_elements(By.NAME,'descr')[0].click()
        web.driver.find_elements(By.NAME,'descr')[0].send_keys(file1.content)
        logger.info('已成功填写简介')
    except Exception as r:
        logger.warning('填写简介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写简介发生错误'
    
    #选择类型
    try:
        select_type = web.driver.find_element('name','type')  
        select_type = Select(select_type)
        if 'anime' in file1.pathinfo.type.lower():
            select_type.select_by_value('403')
        elif 'tv' in file1.pathinfo.type.lower():
            select_type.select_by_value('402')
        elif 'movie' in file1.pathinfo.type.lower():
            select_type.select_by_value('401')
        elif 'show' in file1.pathinfo.type.lower():
            select_type.select_by_value('405')
        elif 'doc' in file1.pathinfo.type.lower():
            select_type.select_by_value('404')
        elif 'sport' in file1.pathinfo.type.lower():
            select_type.select_by_value('407')
        elif 'mv' in file1.pathinfo.type.lower():
            select_type.select_by_value('407')
        elif 'music' in file1.pathinfo.type.lower():
            select_type.select_by_value('406')
        elif 'cartoon' in file1.pathinfo.type.lower():
            select_type.select_by_value('403')
        else:
            select_type.select_by_value('407')
    except Exception as r:
        logger.warning('选择类型发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择类型发生错误'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择媒介
    try:
        select_sel = web.driver.find_element('name','medium_sel')    
        select_sel_ob = Select(select_sel)    
        if file1.type=='WEB-DL':
            select_sel_ob.select_by_value('2')
        elif 'webrip' in file1.type.lower():
            select_sel_ob.select_by_value('1')
        elif 'dvdrip' in file1.type.lower():
            select_sel_ob.select_by_value('4')
        elif 'rip' in file1.type.lower():
            select_sel_ob.select_by_value('1')
        elif 'hdtv'in file1.type.lower():
            select_sel_ob.select_by_value('3')
        elif 'remux' in file1.type.lower():
            select_sel_ob.select_by_value('6')
        else:
            select_sel_ob.select_by_value('6')
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
            select_codec_sel_ob.select_by_value('1')
        elif file1.Video_Format=='H265':
            select_codec_sel_ob.select_by_value('2')
        elif file1.Video_Format=='x265':
            select_codec_sel_ob.select_by_value('2')
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
            select_source_sel_ob.select_by_value('7')
        elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'TrueHD Atmos' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('1')
        elif 'LPCM' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('4')
        elif 'TrueHD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('1')
        elif 'FLAC' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('5')
        elif 'APE' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('8')
        elif 'MP3' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('6')
        elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('3')
        elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'DTS' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'WAV' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('9')
        elif 'M4A' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('9')
        else:
            select_source_sel_ob.select_by_value('9')
    except Exception as r:
        logger.warning('选择音频编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择音频编码发生错误'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    try:
        select_team_sel = web.driver.find_element('name','standard_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if '8K' in file1.standard_sel:
            select_team_sel_ob.select_by_value('1')
        elif '2160' in file1.standard_sel:
            select_team_sel_ob.select_by_value('1')
        elif '1080p' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '1080i' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '720' in file1.standard_sel:
            select_team_sel_ob.select_by_value('3')
        elif '480' in file1.standard_sel:
            select_team_sel_ob.select_by_value('4')
        else:
            select_team_sel_ob.select_by_value('5')
    except Exception as r:
        logger.warning('选择分辨率发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择分辨率发生错误'
    logger.info('已成功选择分辨率为'+file1.standard_sel)

    #选择制作组
    try:
        select_team_sel = web.driver.find_element('name','team_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if 'CARPT' in file1.sub.upper():
            select_team_sel_ob.select_by_value('1')
        elif 'WIKI' in file1.sub.upper():
            select_team_sel_ob.select_by_value('2')
        elif 'CMCT' in file1.sub.upper():
            select_team_sel_ob.select_by_value('3')
        elif 'M-TEAM' in file1.sub.upper() or 'MTEAM' in file1.sub.upper():
            select_team_sel_ob.select_by_value('4')
        else:
            select_team_sel_ob.select_by_value('5')
    except Exception as r:
        logger.warning('选择制作组发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择制作组发生错误'
    logger.info('制作组已成功选择'+file1.sub)
    
    try:
        if 'carpt' in file1.pathinfo.exclusive:
            checkbox=web.driver.find_elements(By.NAME,'tags[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='1':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择禁转')
    except Exception as r:
        logger.warning('选择禁转错误，错误信息: %s' %(r))

    try:
        if 'carpt' in file1.sub.lower():
            checkbox=web.driver.find_elements(By.NAME,'tags[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='3':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官方')
    except Exception as r:
        logger.warning('选择官方发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择官方发生错误'

    try:
        if '国' in file1.language or '中' in file1.language:
            checkbox=web.driver.find_elements(By.NAME,'tags[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='5':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择国语')
    except Exception as r:
        logger.warning('选择国语发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择国语发生错误'

    try:
        if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
            checkbox=web.driver.find_elements(By.NAME,'tags[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='6':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择中字')
    except Exception as r:
        logger.warning('选择中字发生错误，错误信息: %s' %(r))    

    

    try:
        if web.site.uplver==1:
            checkbox=web.driver.find_elements(By.NAME,'uplver')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                logger.info('已选择匿名发布')
    except Exception as r:
        logger.warning('选择匿名发布发生错误，错误信息: %s' %(r))


    #a=input('check')
    String_url = web.driver.current_url;
    try:
        web.driver.find_elements(By.ID,'qr')[0].click()
    except Exception as r:
        logger.warning('发布种子发生错误，错误信息: %s' %(r))
        return False,fileinfo+'发布种子发生错误'

    logger.info('已发布成功')

    String_url =finduploadurl(web.driver)

    downloadurl=finddownloadurl(driver=web.driver,elementstr='/html/body/table[2]/tbody/tr[2]/td/table[1]/tbody/tr[9]/td[2]/a')
    if downloadurl=='已存在':
        return True,fileinfo+'种子发布失败,失败原因:种子'+downloadurl+',当前网址:'+web.driver.current_url

    
    recordupload(os.path.join(record_path,web.site.sitename+'_torrent.csv'),file1,String_url,downloadurl)
    if not downloadurl =='':
        res=qbseed(url=downloadurl,filepath=file1.downloadpath,qbinfo=qbinfo,category=file1.pathinfo.category)
        if res:
            return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
        else:
            return True,fileinfo+'种子发布成功,但是添加种子失败,请手动添加种子，种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
    else:
        return False,fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url

    
