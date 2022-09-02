from loguru import logger
import time
import os
from selenium.webdriver.common.keys import Keys
from auto_upload.utils.uploader.upload_tools import *
from selenium.webdriver.support.select import Select
import re
from selenium.webdriver.common.by import By

def hare_upload(web,file1,record_path,qbinfo,basic):

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
        web.driver.find_elements(By.NAME,'name')[0].send_keys(file1.uploadname.replace('  ',' ').replace(' ','.'))
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

    try:
        web.driver.find_elements(By.NAME,'pt_gen[imdb][link]')[0].send_keys(file1.imdburl)
        logger.info('已成功填写imdb链接')
    except Exception as r:
        logger.warning('填写imdb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写imdb链接发生错误'

    try:
        web.driver.find_elements(By.NAME,'pt_gen[douban][link]')[0].send_keys(file1.doubanurl)
        logger.info('已成功填写豆瓣链接')
    except Exception as r:
        logger.warning('填写豆瓣链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写豆瓣链接发生错误'


    try:
        web.driver.find_elements(By.NAME,'pt_gen[bangumi][link]')[0].send_keys(file1.bgmurl)
        logger.info('已成功填写bangumi链接')
    except Exception as r:
        logger.warning('填写bangumi链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写bangumi链接发生错误'
    logger.info('已成功填写bangumi链接')


    try:
        web.driver.find_elements(By.NAME,'url_poster')[0].send_keys(re.findall(r'\[img\](.*)\[/img\]',file1.douban_info))
    except Exception as r:
        logger.warning('填写海报截图发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写海报截图发生错误'
    logger.info('已成功填写海报截图')


    try:
        #web.driver.find_elements(By.NAME,'url_vimages')[0].click()
        web.driver.find_elements(By.NAME,'screenshots')[0].send_keys(file1.screenshoturl.replace('[img]','').replace('[/img]',''))
    except Exception as r:
        logger.warning('填写截图发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写截图发生错误'
    logger.info('已成功填写截图')


    logger.info('正在填写简介,请稍等...')
    try:
        web.driver.find_elements(By.NAME,'descr')[0].send_keys(file1.douban_info)
        logger.info('已成功填写简介')
    except Exception as r:
        logger.warning('填写简介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写简介发生错误'

    try:
        #web.driver.find_elements(By.NAME,'Media_BDInfo')[0].click()
        web.driver.find_elements(By.NAME,'technical_info')[0].send_keys(file1.mediainfo)
    except Exception as r:
        logger.warning('填写mediainfo发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写mediainfo发生错误'
    logger.info('已成功填写mediainfo')


    #选择类型
    try:
        element_type = web.driver.find_elements(By.CLASS_NAME,'layui-select-tips')
        for item in element_type:
            if '电影' in item.text:
                element_type=item
                break
        if type(element_type)==list:
            logger.error('未找到类型选项组件')
            return False,fileinfo+'未找到类型选项组件'
        element_type=element_type.find_elements(By.XPATH,'div/dl/dd')

        if 'anime' in file1.pathinfo.type.lower():
            for item in element_type:
                if '动漫' in item.text:
                    item.click()
                    break
        elif 'tv' in file1.pathinfo.type.lower():
            for item in element_type:
                if '电视剧' in item.text:
                    item.click()
                    break
        elif 'movie' in file1.pathinfo.type.lower():
            for item in element_type:
                if '电影' in item.text:
                    item.click()
                    break
        elif 'show' in file1.pathinfo.type.lower():
            for item in element_type:
                if '综艺' in item.text:
                    item.click()
                    break
        elif 'doc' in file1.pathinfo.type.lower():
            for item in element_type:
                if '纪录片' in item.text:
                    item.click()
                    break
        elif 'sport' in file1.pathinfo.type.lower():
            for item in element_type:
                if '体育' in item.text:
                    item.click()
                    break
        elif 'mv' in file1.pathinfo.type.lower():
            for item in element_type:
                if '音乐视频' in item.text:
                    item.click()
                    break
        else:
            for item in element_type:
                if 'Others' in item.text:
                    item.click()
                    break
    except Exception as r:
        logger.warning('选择类型发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择类型发生错误'
    logger.info('已成功填写类型为'+file1.pathinfo.type)
    a=input('check')

    #选择媒介
    try:
        select_sel = web.driver.find_element('name','medium_sel')    
        select_sel_ob = Select(select_sel) 
        if 'remux' in file1.type.lower():
            select_sel_ob.select_by_value('4')
        elif 'bdrip' in file1.type.lower():
            select_sel_ob.select_by_value('6')
        elif file1.type=='WEB-DL':
            select_sel_ob.select_by_value('7')
        elif 'webrip' in file1.type.lower():
            select_sel_ob.select_by_value('8')
        elif file1.type=='HDTV':
            select_sel_ob.select_by_value('5')
        elif 'tvrip' in file1.type.lower():
            select_sel_ob.select_by_value('9')
        elif 'dvdrip' in file1.type.lower():
            select_sel_ob.select_by_value('10')
        elif 'dvd' in file1.type.lower():
            select_sel_ob.select_by_value('3')
        else:
            select_sel_ob.select_by_value('12')
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
            select_codec_sel_ob.select_by_value('2')
        elif file1.Video_Format=='x264':
            select_codec_sel_ob.select_by_value('2')
        elif file1.Video_Format=='H265':
            select_codec_sel_ob.select_by_value('1')
        elif file1.Video_Format=='x265':
            select_codec_sel_ob.select_by_value('1')
        else:
            select_codec_sel_ob.select_by_value('2')
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
            select_source_sel_ob.select_by_value('5')
        elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('1')
        elif 'TrueHD Atmos' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'LPCM' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('6')
        elif 'TrueHD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('2')
        elif 'FLAC' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('7')
        elif 'APE' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('8')
        elif 'MP3' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('10')
        elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('4')
        elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('3')
        elif 'DTS' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('3')
        elif 'WAV' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('9')
        elif 'M4A' in file1.Audio_Format.upper():
            select_source_sel_ob.select_by_value('10')
        else:
            select_source_sel_ob.select_by_value('10')
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
            select_team_sel_ob.select_by_value('3')
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
        select_team_sel = web.driver.find_element('name','source_sel')    #定位到id为browsecat的下拉框并起名为select_ele
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
                select_team_sel_ob.select_by_value('9')
                logger.info('国家信息已选择'+file1.country)
            elif '英国' in file1.country:
                select_team_sel_ob.select_by_value('9')
                logger.info('国家信息已选择'+file1.country)
            elif '法国' in file1.country:
                select_team_sel_ob.select_by_value('9')
                logger.info('国家信息已选择'+file1.country)
            elif '韩国' in file1.country:
                select_team_sel_ob.select_by_value('10')
                logger.info('国家信息已选择'+file1.country)
            elif '日本' in file1.country:
                select_team_sel_ob.select_by_value('10')
                logger.info('国家信息已选择'+file1.country)
            elif '印度' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            else:
                select_team_sel_ob.select_by_value('3')
                logger.info('未找到资源国家信息，已选择Other')
        else:
            select_team_sel_ob.select_by_value('10')
            logger.info('未找到资源国家信息，已默认日本')
    except Exception as r:
        logger.warning('选择地区发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择地区发生错误'


    

    try:
        if file1.pathinfo.collection==1:
            checkbox=web.driver.find_elements(By.NAME,'pack')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择合集')
    except Exception as r:
        logger.warning('选择合集错误，错误信息: %s' %(r))

    try:
        if 'ssd' in file1.pathinfo.exclusive:
            checkbox=web.driver.find_elements(By.NAME,'exclusive')
            if len(checkbox)>0:
                checkbox=checkbox[0]
                if not checkbox.is_selected():
                    checkbox.click()
                    logger.info('已选择禁转')
    except Exception as r:
        logger.warning('选择禁转错误，错误信息: %s' %(r))


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

    
