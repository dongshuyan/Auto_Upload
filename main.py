from loguru import logger
import os
from auto_upload.utils.para_ctrl.para_ctrl import read_para
from auto_upload.utils.site.site import makesites
from auto_upload.utils.pathinfo.pathinfo import findpathinfo
from auto_upload.utils.seed_machine.seed_machine import start_machine
from auto_upload.utils.img_upload.imgupload import img_upload

@logger.catch
def main():
    os.system('clear')
    logger.info("欢迎使用sauterne开发的Auto_Upload\n")
    yamlinfo=read_para()
    #设置路径，如果有下载文件都下载到screenshot_path
    os.chdir(yamlinfo['basic']['screenshot_path'])
    if yamlinfo['mod']=='img_upload':
        logger.info('正在使用上传图床模式')
        res=img_upload(imgdata=yamlinfo['image hosting'],imglist=yamlinfo['imgfilelist'],host=yamlinfo['img_host'],form=yamlinfo['img_form'])
        logger.info('成功上传图床')
        print(res)

    if yamlinfo['mod']=='upload':

        sites=makesites(yamlinfo['site info'])
        #for item in sites:
        #    sites[item].print()
        
        pathlist=findpathinfo(yamlinfo,sites)
        #for item in pathlist:
        #    item.print()

        start_machine(pathlist,sites,yamlinfo)


if __name__ == '__main__':
    main()