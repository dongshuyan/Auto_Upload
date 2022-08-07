import os
import yaml
def readyaml(file):
    with open(file, encoding='utf-8')as f:
         audata = yaml.load(f, Loader=yaml.FullLoader)
    return audata
    
def write_yaml(au_data):
    file=''
    mod =''
    if 'yaml_path' in au_data:
        file=au_data.pop('yaml_path')
    if 'mod' in au_data    :
        mod =au_data.pop('mod')

    with open(file, "w", encoding='utf-8')as f:
        f.write(yaml.dump(au_data, allow_unicode=True, sort_keys=False))

    if not file=='':
        au_data['yaml_path']=file
    if not mod=='':
        au_data['mod']=mod
