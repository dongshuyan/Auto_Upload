import os
import yaml
from loguru import logger
def readyaml(file):
    with open(file, encoding='utf-8')as f:
         audata = yaml.load(f, Loader=yaml.FullLoader)
    newfile=file+'.bak'
    write_yaml(audata,newfile)
    return audata
    
def write_yaml(au_data,file=''):
    mod =''
    if file=='' and 'yaml_path' in au_data:
        file=au_data.pop('yaml_path')
    if 'mod' in au_data    :
        mod =au_data.pop('mod')
    if file=='':
        logger.error('未找到yaml文件信息,无法写入文件')
        raise ValueError ('未找到yaml文件信息,无法写入文件')

    with open(file, "w", encoding='utf-8')as f:
        f.write(yaml.dump(au_data, allow_unicode=True, sort_keys=False))

    if not file=='' and not '.bak' in file:
        au_data['yaml_path']=file
    if not mod=='':
        au_data['mod']=mod
