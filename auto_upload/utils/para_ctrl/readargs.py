import argparse
import os


def readargs():
    mainpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yaml_path = os.path.join(mainpath,"au.yaml")
    basic_path = os.path.join(mainpath,"basicinfo.yaml")
    parser = argparse.ArgumentParser(description='Weclome AutoUpload')
    parser.add_argument('-u','--upload', action='store_true', default=False, help='Upload local resources automatically')
    parser.add_argument('-s','--sign', action='store_true', default=False, help='Upload local resources automatically')
    parser.add_argument('-iu','--img-upload', action='store_true', default=False, help='Upload local resources automatically')

    parser.add_argument('-ih','--img-host', type=str, help='Choose your img host from the following list. [ptpimg,picgo,chd,smms,pter,emp,femp,imgbox]',choices=['ptpimg','picgo','chd','smms','pter','emp','femp','imgbox'],required=False,default='')
    parser.add_argument('-if','--img-file', nargs='+',help='Choose your img file',action='append',required=False)
    parser.add_argument('-iform','--img-form', help='Choose your img form the following list. [bbcode,img]',choices=['bbcode','img'],required=False,default='img')

    parser.add_argument('-yp','--yaml-path', type=str, help='Path of your au.yaml',required=True,default=yaml_path)
    parser.add_argument('-bp','--basic-path', type=str, help='Path of your basicinfo.yaml',required=False,default=basic_path)
    args = parser.parse_args()
    return args
