from loguru import logger
from auto_upload.utils.para_ctrl.readyaml import write_yaml
import os
from auto_upload.utils.pathinfo.pathinfo import findnum
from auto_upload.utils.mediafile.mediafile import mediafile
from auto_upload.utils.web.web import web
from auto_upload.utils.uploader.auto_upload import auto_upload


def seedmachine_single(pathinfo,sites,pathyaml,basic,qbinfo,imgdata):
    '''
    para:
        pathinfo
        sites 
        pathyaml 用于更新yaml中发布信息
        basic
        qbinfo  
    '''
    logger.info('正在发布路径'+pathinfo.path+'下资源')
    log_error=''
    log_succ=''
    logstr=''
    for pathep in pathinfo.eps:

        #判断此集有没有站点要发布,此集合收纳还没有发布过本集的站点
        site_upload=[]
        for siteitem in sites:
            #发布过此集的站点略过
            if sites[siteitem].enable==1 and not( eval('pathinfo.'+siteitem+'_max_done==10000')) and not eval('pathep in pathinfo.'+siteitem+'_done'):
                site_upload.append(sites[siteitem])

        #如果没有站点要发布就略过本集
        if len(site_upload)==0:
            continue

        ls = os.listdir(pathinfo.path)
        filepath=''
        for i in ls:
            c_path=os.path.join(pathinfo.path, i)
            if (os.path.isdir(c_path)) or (i.startswith('.')) or (not(  os.path.splitext(i)[1].lower()== ('.mp4') or os.path.splitext(i)[1].lower()== ('.mkv')  or os.path.splitext(i)[1].lower()== ('.avi') or os.path.splitext(i)[1].lower()== ('.ts')    )):
                continue
            if int(findnum(i)[0])==pathep:
                filepath=c_path
                break

        if filepath=='':
            logger.error('未找到文件夹'+pathinfo.path+'下第'+str(pathep)+'集资源')
            raise ValueError ('未找到文件夹'+pathinfo.path+'下第'+str(pathep)+'集资源')

        #获取file全部信息
        file1=mediafile(filepath,pathinfo,basic,imgdata)
        if not pathinfo.imdb_url=='' and pathyaml['imdb_url']==None:
            pathyaml['imdb_url']=pathinfo.imdb_url
        
        file1.getfullinfo()
        logger.info('正在发布路径'+pathinfo.path+'下第'+str(pathep)+'集资源:'+filepath)
        for siteitem in site_upload:
            if siteitem.enable==0:
                continue
            logger.info('正在'+siteitem.sitename+'站点发布路径'+pathinfo.chinesename+'第'+str(pathep)+'集资源')
            
            upload_success=False
            uploadtime=0
            while upload_success==False and uploadtime<3:
                uploadtime=uploadtime+1
                logger.info('第'+str(uploadtime)+'次尝试发布')
                print("正在准备登录"+siteitem.sitename)

                suc=False
                trynum=0
                while suc==False:
                    trynum=trynum+1
                    if trynum>5:
                        logger.warning(siteitem.sitename+'站点登录失败')
                    if trynum==1:
                        web1=web(site=siteitem,headless=True)
                    else:
                        web1=web(site=siteitem,headless=False)
                    web1.login_cookie()
                    suc=web1.login

                if suc==False:
                    continue

                try:
                    upload_success,logstr=auto_upload(web1,file1,basic['record_path'],qbinfo)
                except Exception as r:
                    logger.warning('发布资源发生错误，错误信息: %s' %(r))
                    upload_success=False

                del(web1)
                if not upload_success:
                    logger.warning(siteitem.sitename+'第'+str(uploadtime)+'次发布任务失败')
                    logger.warning(logstr)

            if not upload_success:
                logger.warning(siteitem.sitename+'发布任务失败，本站暂停发种')
                siteitem.enable=0
                log_error=log_error+logstr+'\n'
                logger.warning(logstr)
            else:
                log_succ=log_succ+logstr+'\n'
                logger.info(logstr)
                #记录已发布的种子
                exec('pathinfo.'+siteitem.sitename+'_done.append(pathep)')
                exec('pathinfo.'+siteitem.sitename+'_done.sort()')
                exec('pathyaml["'+siteitem.sitename+'"]=",".join([str(i) for i in pathinfo.'+siteitem.sitename+'_done])')
                #deletetorrent(basic['screenshot_path'])
            #a=input('check')
            

    logger.info('路径'+pathinfo.path+'下资源已全部发布完毕')
    return log_error,log_succ

def seedmachine(pathinfo,sites,pathyaml,basic,qbinfo,imgdata):
    '''
    para:
        pathinfo
        sites 
        pathyaml 用于更新yaml中发布信息
        basic
        qbinfo  
    '''
    logger.info('正在发布路径'+pathinfo.path+'下资源')
    log_error=''
    log_succ=''
    logstr=''

    site_upload=[]
    for siteitem in sites:
        #发布过此集的站点略过
        if sites[siteitem].enable==1 and not( eval('pathinfo.'+siteitem+'_max_done==10000')) and not eval('-1 in pathinfo.'+siteitem+'_done'):
            site_upload.append(sites[siteitem])

    #如果没有站点要发布就略过本集
    if len(site_upload)==0:
        logger.info('路径'+pathinfo.path+'下资源已全部发布完毕')
        return log_error,log_succ


    #获取file全部信息
    file1=mediafile(pathinfo.path,pathinfo,basic,imgdata)
    if not pathinfo.imdb_url=='' and pathyaml['imdb_url']==None:
        pathyaml['imdb_url']=pathinfo.imdb_url

    logger.info('正在'+siteitem+'站点发布路径'+pathinfo.path+'下资源')
    file1.getfullinfo()

    for siteitem in site_upload:
        if siteitem.enable==0:
            continue
        logger.info('正在'+siteitem.sitename+'站点发布'+pathinfo.chinesename+'资源')
        upload_success=False
        uploadtime=0
        while upload_success==False and uploadtime<3:
            uploadtime=uploadtime+1
            logger.info('第'+str(uploadtime)+'次尝试发布')
            print("正在准备登录"+siteitem.sitename)

            suc=False
            trynum=0
            while suc==False:
                trynum=trynum+1
                if trynum>5:
                    logger.warning(siteitem.sitename+'站点登录失败')
                if trynum==1:
                    web1=web(site=siteitem,headless=True)
                else:
                    web1=web(site=siteitem,headless=False)
                web1.login_cookie()
                suc=web1.login

            if suc==False:
                continue

            upload_success,logstr=auto_upload(web1,file1,basic['record_path'],qbinfo)
            del(web1)
            if not upload_success:
                logger.warning(siteitem.sitename+'第'+str(uploadtime)+'次发布任务失败')
                logger.warning(logstr)

        if not upload_success:
            logger.warning(siteitem.sitename+'发布任务失败，本站暂停发种')
            siteitem.enable=0
            log_error=log_error+logstr+'\n'
            logger.warning(logstr)
        else:
            log_succ=log_succ+logstr+'\n'
            logger.info(logstr)
            #记录已发布的种子
            exec('pathinfo.'+siteitem.sitename+'_done.append(-1)')
            exec('pathinfo.'+siteitem.sitename+'_done.sort()')
            exec('pathyaml["'+siteitem.sitename+'"]=",".join([str(i) for i in pathinfo.'+siteitem.sitename+'_done])')
            #deletetorrent(basic['screenshot_path'])
        #a=input('check')
       

    logger.info('路径'+pathinfo.path+'下资源已全部发布完毕')
    return log_error,log_succ



def start_machine(pathlist,sites,yamlinfo):
    log_allsucc=''
    log_allerror=''
    for path in pathlist:
        if path.enable==0:
            logger.info('路径'+path.path+'的enable被设置为0，已忽略')
            continue
        if (path.type=='anime' or path.type=='tv') and path.collection==0:
            log_error,log_succ=seedmachine_single(path,sites,yamlinfo['path info'][path.pathid],yamlinfo['basic'],yamlinfo['qbinfo'],yamlinfo['image hosting'])
        else:
            log_error,log_succ=seedmachine(path,sites,yamlinfo['path info'][path.pathid],yamlinfo['basic'],yamlinfo['qbinfo'],yamlinfo['image hosting'])
        write_yaml(yamlinfo)
        if not log_succ=='':
            log_allsucc=log_allsucc+log_succ+'\n'
            logger.info(log_succ)
        if not log_error=='':
            log_allerror=log_allerror+log_error+'\n'
            logger.error(log_error)


