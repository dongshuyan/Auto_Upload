# Auto_Upload  
自动将本地资源发布到PT站  
Upload local resources to PT trackers automatically.  

## 使用说明  
### Step1.安装auto_upload 
``` bash 
pip3 install auto_upload  
```
### 配置环境&文件  
#### 1.需要本地安装Chrome且升级到最新正式版本（以Mac为例，2020.08.06最新正式版为104.0.5112.79）  

#### 2.本地新建一个工作目录，例如路径为:/Users/Desktop/auto_upload  

#### 3.在2种工作路径文件夹下，再新建三个文件夹:"cookies_path","screenshot_path","record_path"  
cookies_path将用来存放站点cookie文件，文件名需要命名为cookie_站点.js。(例如:cookie_lemonhd.json,cookie_pter.json等)  
screenshot_path将用来存放视频截图，种子等临时文件  
record_path将用来存放发种记录 

#### 4.获取cookie并存入文件 工作目录/cookies_path/cookie_站点.js 中  
js格式的cookie推荐使用插件"EditThisCookie"获取  
EditThisCookie插件官网:http://www.editthiscookie.com/
Chrome下EditThisCookie安装网址:https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg  
Edge下EditThisCookie安装网址:https://microsoftedge.microsoft.com/addons/detail/editthiscookie/jhampopgcdhehhkbeljdbfdbkfkmolbh?hl=zh-CN  

#### 5.在文件夹中新建配置文件au.yaml
配置文件可以样例[au.yaml.example](https://github.com/dongshuyan/Auto_Upload/blob/main/au.yaml.example)填写  

建立完成后在工作目录下应该有三个文件夹以及一个au.yaml位置文件，如下图  
![Img_Demo](https://img.picgo.net/2022/08/06/dir.jpg)

### 运行脚本
#### 1.自动发种
``` bash
auto_upload -yp '工作目录/au.yaml' -u
```

#### 2.本地图片自动上传图床
``` bash
auto_upload -yp '工作目录/au.yaml' -iu -ih 图床名称 -if  '图片路径1' '图片路径2'
```
图床名称目前仅支持（排名无先后）：
ptpimg
picgo
chd
imgbox
pter
smms

##配置文件au.yaml详细说明






