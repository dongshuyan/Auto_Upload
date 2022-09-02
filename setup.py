from setuptools import setup, find_packages
import io

setup(
    name = "auto_upload",     
    version = "0.0.79", 
    keywords = ["pip", "auto_upload","auto","upload","PT","private tracker"],            
    description = "Upload local resources to PT trackers automatically.",    
    long_description=io.open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license = "MIT Licence",    

    entry_points = {
        'console_scripts': [
            'auto_upload=auto_upload.main:main',
            'au=auto_upload.main:main',
        ],
    },

    url = "https://github.com/dongshuyan/Auto_Upload", 
    author = "sauterne",            
    author_email = "ssauterne@qq.com",

    packages = find_packages(),
    include_package_data = True,
    exclude_package_data = {'': ['__pycache__']},

    platforms = "any",
    python_requires = '>=3.7.0',
    install_requires = ["loguru","pathlib","typing","pyyaml","requests","bs4","lxml","datetime","selenium","qbittorrent-api","undetected_chromedriver","function_controler","ddddocr"]
)