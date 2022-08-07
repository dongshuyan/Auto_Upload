from loguru import logger
import time
import os
from selenium.webdriver.common.keys import Keys
from auto_upload.utils.uploader.upload_tools import *
from selenium.webdriver.support.select import Select

def lemonhd_upload(web,file1,record_path,qbinfo):
    if 'anime' in file1.pathinfo.type.lower():
        return lemonhd_upload_anime(web,file1,record_path,qbinfo)
    elif 'tv' in file1.pathinfo.type.lower():
        return lemonhd_upload_tv(web,file1,record_path,qbinfo)
    elif 'movie' in file1.pathinfo.type.lower():
        return lemonhd_upload_tv(web,file1,record_path,qbinfo)

def lemon_check(web):
    logger.info('正在自动审核')
    #自动审核
    try:
        checkbox=web.driver.find_elements_by_name('check_type')[0]
        if not checkbox.is_selected():
            checkbox.click()
        logger.info('自动选择审核通过')
        time.sleep(2)
        web.driver.find_elements_by_id('qr')[0].click()
        logger.info('已审核')
        return True
    except Exception as r:
        logger.info('审核失败')
        return False

def lemonhd_upload_anime(web,file1,record_path,qbinfo):

    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+web.site.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+web.site.sitename

    web.driver.get(web.site.uploadurl)
        
    logger.info('正在'+web.site.sitename+'发布种子...')
    web.driver.find_element_by_class_name('file').send_keys(file1.torrentpath);
    logger.info('已成功上传种子')
    
    if len(web.driver.find_elements_by_name('name'))<=0:
        web.driver.execute_script("window.scrollBy(0,300)")
    #web.driver.find_elements_by_name('small_descr')[0].click()
    web.driver.find_elements_by_name('small_descr')[0].send_keys(file1.small_descr)
    logger.info('已成功填写副标题')
    
    #web.driver.find_elements_by_name('douban_url')[0].click()
    web.driver.find_elements_by_name('douban_url')[0].send_keys(file1.doubanurl)
    logger.info('已成功填写豆瓣链接')
    
    #web.driver.find_elements_by_name('url')[0].click()
    web.driver.find_elements_by_name('url')[0].send_keys(file1.imdburl)
    logger.info('已成功填写IMDb链接')
    
    #web.driver.find_elements_by_name('bangumi_url')[0].click()
    web.driver.find_elements_by_name('bangumi_url')[0].send_keys(file1.bgmurl)
    logger.info('已成功填写Bangumi链接')
    
    #web.driver.find_elements_by_name('anidb_url')[0].click()
    web.driver.find_elements_by_name('anidb_url')[0].send_keys(file1.anidburl)
    logger.info('已成功填写Anidb链接')
    
    #web.driver.find_elements_by_name('cn_name')[0].click()
    web.driver.find_elements_by_name('cn_name')[0].send_keys(file1.chinesename)
    logger.info('已成功填写中文名')
    
    #web.driver.find_elements_by_name('en_name')[0].click()
    web.driver.find_elements_by_name('en_name')[0].send_keys(file1.englishname)
    logger.info('已成功填写英文名')
    
    #web.driver.find_elements_by_name('descr')[0].click()
    web.driver.find_elements_by_name('descr')[0].send_keys(file1.content)
    logger.info('已成功填写简介')
    
    #web.driver.find_elements_by_name('year')[0].click()
    web.driver.find_elements_by_name('year')[0].send_keys(str(file1.year))
    logger.info('已成功填写年份',str(file1.year))

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
        is_complete_checkbox=web.driver.find_elements_by_name('is_complete')[0]
        if not is_complete_checkbox.is_selected():
            is_complete_checkbox.click()
        logger.info('已成功选择未完结')

    if file1.pathinfo.collection==0:
        #web.driver.find_elements_by_name('series')[0].click()
        web.driver.find_elements_by_name('series')[0].send_keys('第'+file1.episodename+'话')
    elif file1.pathinfo.complete==1:
        web.driver.find_elements_by_name('series')[0].send_keys('TV '+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2)+' Fin')
    else:
        web.driver.find_elements_by_name('series')[0].send_keys('TV '+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2))
    logger.info('已成功填写集数')

    #web.driver.find_elements_by_name('source_author')[0].click()
    web.driver.find_elements_by_name('source_author')[0].send_keys(file1.sub)
    logger.info('已成功填写制作组')

    

    #选择媒介
    select_animate_category = web.driver.find_element('name','animate_category')   
    select_animate_category_ob = Select(select_animate_category)   
    select_animate_category_ob.select_by_value('7')

    #选择编码
    select_codec_sel = web.driver.find_element('name','codec_sel')    
    select_codec_sel_ob = Select(select_codec_sel)    
    select_codec_sel_ob.select_by_value('1')
    if file1.Video_Format=='H264':
        select_codec_sel_ob.select_by_value('1')
    elif file1.Video_Format=='x264':
        select_codec_sel_ob.select_by_value('12')
    elif file1.Video_Format=='H265':
        select_codec_sel_ob.select_by_value('10')
    elif file1.Video_Format=='x265':
        select_codec_sel_ob.select_by_value('11')

    logger.info('已成功选择音频编码'+file1.Video_Format)

    #选择音频编码
    select_audiocodec_sel = web.driver.find_element('name','audiocodec_sel')    
    select_audiocodec_sel_ob = Select(select_audiocodec_sel)   
    select_audiocodec_sel_ob.select_by_value('8')
    logger.info('已成功选择音频编码AAC')

    #选择分辨率
    select_standard_sel = web.driver.find_element('name','standard_sel')   
    select_standard_sel_ob = Select(select_standard_sel)   
    select_standard_sel_ob.select_by_value('2')
    logger.info('已成功选择分辨率1080P')

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
            select_team_sel_ob.select_by_value('6')
            logger.info('未找到资源国家信息，已默认日本')
    except Exception as r:
        logger.warning('选择地区发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择地区发生错误'

    #选择来源
    select_original = web.driver.find_element('name','original')    
    select_original_ob = Select(select_original)
    if file1.pathinfo.transfer==1:
        select_original_ob.select_by_value('1')
        logger.info('已选择来源为转载')
        web.driver.find_elements_by_name('from_url')[0].send_keys(file1.from_url)
        logger.info('已成功填写转载地址')
    elif file1.pathinfo.transfer==0:
        select_original_ob.select_by_value('2')
        logger.info('已选择来源为原创')
    else:
        select_original_ob.select_by_value('1')
        logger.info('已默认来源为转载')
        web.driver.find_elements_by_name('from_url')[0].send_keys(file1.from_url)
        logger.info('已成功填写转载地址')

    
    try:
        if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
            checkbox=web.driver.find_elements_by_name('tag_zz')[0]
            if not checkbox.is_selected():
                checkbox.click()
            logger.info('已选择中字')
    except Exception as r:
        logger.warning('选择中字发生错误，错误信息: %s' %(r))

    try:
        if web.site.uplver==1:
            checkbox=web.driver.find_elements_by_name('uplver')[0]
            if not checkbox.is_selected():
                checkbox.click()
            logger.info('已选择匿名发布')
    except Exception as r:
        logger.warning('选择匿名发布发生错误，错误信息: %s' %(r))

    
    String_url = web.driver.current_url;
    web.driver.find_elements_by_id('qr')[0].click()
    logger.info('已发布成功')

    String_url =finduploadurl(web.driver)

    downloadurl=finddownloadurl(driver=web.driver,elementstr='/html/body/table[2]/tbody/tr[2]/td/table[1]/tbody/tr[10]/td[2]/a[2]')
    
    recordupload(os.path.join(record_path,web.site.sitename+'_torrent.csv'),file1,String_url,downloadurl)

    if not downloadurl =='':

        res=qbseed(url=downloadurl,filepath=file1.path,qbinfo=qbinfo)
        if res:
            logger.info(fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url)
        else:
            logger.warning(fileinfo+'添加种子失败,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url)
            return False,fileinfo+'添加种子失败,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
    else:
        logger.warning(fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url)
        return False,fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url
    
    res=lemon_check(web)
    if res:
        logger.info('成功审核第'+file1.episodename+'集的资源')
        infostr=fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url+'且成功审核第'+file1.episodename+'集的资源'
        logger.info(infostr)
        return True,infostr
    else:
        logger.info('未成功审核第'+file1.episodename+'集的资源')
        return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url+'但未成功审核第'+file1.episodename+'集的资源'
    



    