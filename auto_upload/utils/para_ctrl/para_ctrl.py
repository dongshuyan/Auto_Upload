from auto_upload.utils.para_ctrl.readyaml import readyaml
from auto_upload.utils.para_ctrl.readargs import readargs
from auto_upload.utils.para_ctrl.readyaml import write_yaml
import os
from loguru import logger

def read_para():
    args = readargs()

    iu=0#img upload
    su=0#sign
    ru=0#resources upload
    if not args.img_upload+args.sign+args.upload==1:
        logger.error('参数输入错误，上传模式 -u,签到模式 -s,上传图床模式 -iu,必须且只能选择一个。')
        raise ValueError ('参数输入错误，上传模式 -u,签到模式 -s,上传图床模式 -iu,必须且只能选择一个。')


    au_data   = readyaml(args.yaml_path)
    basic_data = readyaml(args.basic_path)
    merge_para(basic_data,au_data)

    if 'basic' in au_data and 'workpath' in au_data['basic']:
        if not os.path.exists(au_data['basic']['workpath']):
            logger.info('检测到workpath目录并未创建，正在新建文件夹：'+au_data['basic']['workpath'])
            os.makedirs(au_data['basic']['workpath'])
        itemlist=['record_path','cookies_path','screenshot_path']
        for item in itemlist:
            if not item in au_data['basic']:
                au_data['basic'][item]=os.path.join(au_data['basic']['workpath'],item)
                if not os.path.exists(au_data['basic'][item]):
                    logger.info('检测到'+item+'目录并未创建，正在新建文件夹：'+au_data['basic'][item])
                    os.makedirs(au_data['basic'][item])

    if 'basic' in au_data and 'cookies_path' in au_data['basic']:
        for item in au_data['site info']:
            if not 'cookiefile' in au_data['site info'][item]:
                au_data['site info'][item]['cookiefile']=os.path.join(au_data['basic']['cookies_path'],'cookie_'+item+'.json')
    
    au_data['yaml_path']=args.yaml_path
    write_yaml(au_data)
    
    au_data['mod']=args.img_upload*'img_upload'+args.sign*'sign'+args.upload*'upload'

    if args.upload:
        if not 'path info' in au_data or len(au_data['path info'])==0:
            logger.error('参数输入错误，发布资源请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，发布资源请至少输入一个本地文件地址')
        for item in au_data['path info']:
            if not 'path' in au_data['path info'][item] or au_data['path info'][item]['path']==None or au_data['path info'][item]['path']=='':
                logger.error('参数输入错误，'+item+'请至少输入一个本地文件地址')
                raise ValueError ('参数输入错误，'+item+'请至少输入一个本地文件地址')
            if 'type' in au_data['path info'][item] and not ( au_data['path info'][item]['type'].lower()=='anime' or au_data['path info'][item]['type'].lower()=='tv' or au_data['path info'][item]['type'].lower()=='movie'):
                logger.error('参数输入错误，'+item+'的type类型暂不支持')
                raise ValueError ('参数输入错误，'+item+'的type类型暂不支持')


    
    if args.img_upload:
        if 'img_host' in args and not args.img_host=='':
            au_data['img_host']=args.img_host
        else:
            au_data['img_host']=''

        if 'img_form' in args and not args.img_form=='':
            au_data['img_form']=args.img_form
        else:
            au_data['img_form']='img'

        filelist=[]
        if 'img_file' in args and args.img_file==None:
            logger.error('参数输入错误，上传图片请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，上传图片请至少输入一个本地文件地址')
        for item in args.img_file:
            for imgitem in item:
                if not imgitem in filelist:
                    filelist.append(imgitem)
        if len(filelist)==0:
            logger.error('参数输入错误，上传图片请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，上传图片请至少输入一个本地文件地址')
        au_data['imgfilelist']=filelist





    return au_data

def merge_para(dict1,dict2):
    '''
    将dict1中的内容合并入dict2,如果有相同内容保持dict2
    '''
    if not (type(dict1)==dict and type(dict2)==dict):
        return 
    for item in dict1:
        if item in dict2:
            merge_para(dict1[item],dict2[item])
        else:
            dict2[item]=dict1[item]

