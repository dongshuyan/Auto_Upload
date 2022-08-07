from urllib.parse import urlparse
from bs4 import BeautifulSoup
from auto_upload.utils.uploader.pter_upload import pter_upload
from auto_upload.utils.uploader.lemonhd_upload import lemonhd_upload



def auto_upload(driver,file,record_path,qbinfo):
    return eval(driver.site.sitename+'_upload(driver,file,record_path,qbinfo)')