from urllib.parse import urlparse
from bs4 import BeautifulSoup
from auto_upload.utils.uploader.pter_upload import pter_upload
from auto_upload.utils.uploader.lemonhd_upload import lemonhd_upload
from auto_upload.utils.uploader.hdsky_upload import hdsky_upload
from auto_upload.utils.uploader.audience_upload import audience_upload
from auto_upload.utils.uploader.piggo_upload import piggo_upload
from auto_upload.utils.uploader.ssd_upload import ssd_upload
from auto_upload.utils.uploader.hdpt_upload import hdpt_upload
from auto_upload.utils.uploader.carpt_upload import carpt_upload
from auto_upload.utils.uploader.ptnap_upload import ptnap_upload
from auto_upload.utils.uploader.wintersakura_upload import wintersakura_upload
from auto_upload.utils.uploader.hdfans_upload import hdfans_upload
#from auto_upload.utils.uploader.hare_upload import hare_upload



def auto_upload(driver,file,record_path,qbinfo):
    return eval(driver.site.sitename+'_upload(driver,file,record_path,qbinfo)')