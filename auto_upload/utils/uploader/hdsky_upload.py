from loguru import logger
import time
import os
from selenium.webdriver.common.keys import Keys
from auto_upload.utils.uploader.upload_tools import *
from selenium.webdriver.support.select import Select
import re
from selenium.webdriver.common.by import By

def hdsky_upload(web,file1,record_path,qbinfo):

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

    try:
        #web.driver.find_elements(By.NAME,'small_descr')[0].click()
        web.driver.find_elements(By.NAME,'small_descr')[0].send_keys(file1.small_descr+file1.pathinfo.exinfo)
        logger.info('已成功填写副标题')
    except Exception as r:
        logger.warning('填写副标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写副标题发生错误'
    try:
        #web.driver.find_elements(By.NAME,'url_douban')[0].click()
        web.driver.find_elements(By.NAME,'url_douban')[0].send_keys(file1.doubanurl)
        logger.info('已成功填写豆瓣链接')
    except Exception as r:
        logger.warning('填写豆瓣链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写豆瓣链接发生错误'

    try:
        #web.driver.find_elements(By.NAME,'url')[0].click()
        web.driver.find_elements(By.NAME,'url')[0].send_keys(file1.imdburl)
        logger.info('已成功填写IMDb链接')
    except Exception as r:
        logger.warning('填写IMDb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写IMDb链接发生错误'

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
            select_type.select_by_value('405')
        elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==1:
            if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
                select_type.select_by_value('411')
            else:
                select_type.select_by_value('413')
        elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
            if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
                select_type.select_by_value('402')
            else:
                select_type.select_by_value('412')
        elif 'movie' in file1.pathinfo.type.lower():
            select_type.select_by_value('401')
        else:
            select_type.select_by_value('409')

    except Exception as r:
        logger.warning('选择类型发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择类型发生错误'

    #选择媒介
    try:
        select_sel = web.driver.find_element('name','medium_sel')    
        select_sel_ob = Select(select_sel)    
        if file1.type=='WEB-DL':
            select_sel_ob.select_by_value('11')
        elif 'rip' in file1.type.lower() or file1.type=='bluray'  :
            select_sel_ob.select_by_value('7')
        elif file1.type=='HDTV':
            select_sel_ob.select_by_value('5')
        elif file1.type=='remux':
            select_sel_ob.select_by_value('3')
        else:
            select_sel_ob.select_by_value('7')
        logger.info('已成功选择质量为'+file1.type)
    except Exception as r:
        logger.warning('选择媒介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择媒介发生错误'


    #选择编码
    try:
        select_codec_sel = web.driver.find_element('name','codec_sel') 
        select_codec_sel_ob = Select(select_codec_sel) 
        select_codec_sel_ob.select_by_value('1')
        if file1.Video_Format=='H264':
            select_codec_sel_ob.select_by_value('1')
        elif file1.Video_Format=='x264':
            select_codec_sel_ob.select_by_value('10')
        elif file1.Video_Format=='H265':
            select_codec_sel_ob.select_by_value('12')
        elif file1.Video_Format=='x265':
            select_codec_sel_ob.select_by_value('13')
        logger.info('已成功选择编码为'+file1.Video_Format)
    except Exception as r:
        logger.warning('选择编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择编码发生错误'

    #选择音频编码
    try:
        select_source_sel = web.driver.find_element('name','audiocodec_sel')   
        select_source_sel_ob = Select(select_source_sel)    
        if file1.Audio_Format.upper()=='AAC':
            select_source_sel_ob.select_by_value('6')
        elif 'DTS-HDMA:X 7.1' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('16')
        elif 'DTS-HDMA' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('10')
        elif 'TrueHD Atmos' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('17')
        elif 'LPCM' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('13')
        elif 'TrueHD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('11')
        elif 'DTS-HD HR' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('14')
        elif 'PCM' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('19')
        elif 'FLAC' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('1')
        elif 'APE' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'MP3' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('4')
        elif 'OGG' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('5')
        elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('12')
        elif 'DTS' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('3')
        elif 'WAV' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('15')
        elif 'DSD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('18')
        elif 'Dolby Digital Plus Dolby Atmos' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('21')
        elif 'Dolby Digital Plus' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('20')
        else:
            select_source_sel_ob.select_by_value('7')
    except Exception as r:
        logger.warning('选择音频编码发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择音频编码发生错误'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    try:
        select_team_sel = web.driver.find_element('name','standard_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if '2160' in file1.standard_sel:
            select_team_sel_ob.select_by_value('5')
        elif '1080p' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('1')
        elif '1080i' in file1.standard_sel.lower():
            select_team_sel_ob.select_by_value('2')
        elif '720' in file1.standard_sel:
            select_team_sel_ob.select_by_value('3')
        elif '480' in file1.standard_sel:
            select_team_sel_ob.select_by_value('4')
        else:
            select_team_sel_ob.select_by_value('1')
    except Exception as r:
        logger.warning('选择分辨率发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择分辨率发生错误'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    #选择制作组
    try:
        select_team_sel = web.driver.find_element('name','team_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if 'HDSKY' in file1.sub.upper():
            select_team_sel_ob.select_by_value('6')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDS3D' in file1.sub.upper():
            select_team_sel_ob.select_by_value('28')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDSTV' in file1.sub.upper():
            select_team_sel_ob.select_by_value('9')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDSWEB' in file1.sub.upper() and file1.pathinfo.collection==1:
            select_team_sel_ob.select_by_value('35')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDSWEB' in file1.sub.upper():
            select_team_sel_ob.select_by_value('31')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDSPAD' in file1.sub.upper():
            select_team_sel_ob.select_by_value('18')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDSCD' in file1.sub.upper():
            select_team_sel_ob.select_by_value('22')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'hdspecial' in file1.sub.lower():
            select_team_sel_ob.select_by_value('34')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'BMDRU' in file1.sub.upper():
            select_team_sel_ob.select_by_value('30')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'AREA11' in file1.sub.upper():
            select_team_sel_ob.select_by_value('25')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDSAB' in file1.sub.upper():
            select_team_sel_ob.select_by_value('36')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif 'HDS' in file1.sub.upper():
            select_team_sel_ob.select_by_value('1')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='12':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择官组')
        elif file1.transfer==0:
            select_team_sel_ob.select_by_value('24')
        elif file1.transfer==1:
            select_team_sel_ob.select_by_value('27')
        else:
            select_team_sel_ob.select_by_value('27')
    except Exception as r:
        logger.warning('选择制作组发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择制作组发生错误'
    logger.info('制作组已成功选择'+file1.transfer*'转载'+(1-file1.transfer)*'原创')
    

    try:
        if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
            #checkbox=web.driver.find_elements(By.XPATH,'/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[12]/td[2]/input[7]')
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='6':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择中字')
    except Exception as r:
        logger.warning('选择中字发生错误，错误信息: %s' %(r))

    try:
        if '国' in file1.language or '中' in file1.language:
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='5':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择国语')
    except Exception as r:
        logger.warning('选择国语发生错误，错误信息: %s' %(r))

    try:
        if 'hdsky' in file1.pathinfo.exclusive:
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='2':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择禁转')
    except Exception as r:
        logger.warning('选择禁转错误，错误信息: %s' %(r))

    try:
        if file1.transfer==0:
            checkbox=web.driver.find_elements(By.NAME,'option_sel[]')
            if len(checkbox)>0:
                for item in checkbox:
                    if 'get_attribute' in dir(item) and item.get_attribute('value')=='14':
                        if not item.is_selected():
                            item.click()
                            logger.info('已选择自制')
    except Exception as r:
        logger.warning('选择自制错误，错误信息: %s' %(r))

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

    
