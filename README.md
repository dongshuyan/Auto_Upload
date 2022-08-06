## Auto_Upload  
自动将本地资源发布到PT站  
Upload local resources to PT trackers automatically.  

## 功能说明  
### 命令行实现将本地图片上传到图床  
### 自动检测本地未发布的资源并发布到站点，并下载到Qbittorrent  
包括了以下功能:  
- 根据配置文件分析待发布资源的中英文名
- 根据配置文件分析已经发布的资源并自动找到未发布的资源
- 将未发布的资源有序发布
- 自动获取待发布资源的豆瓣链接/动漫资源的bgm链接
- 自动获取待发布资源的豆瓣简介
- 自动获取待发布资源的截图并上传到图床获取bbcode
- 自动获取待发布资源的mediainfo信息
- 自动制作种子
- 根据上述信息自动发布到各个站点（分集发布/打包发布）
- 自动获取下载链接并传递给Qbittorrent做种
- 自动记录发布资源信息生成excel表格(csv文件)
- 自动统计目前已发布的总量(可以用来统计每月发种数量)



## 安装Auto_Upload自动发种机

`Auto_Upload自动发种机`可以在任何具有`Python`环境的系统上使用，下面讲解下在各个系统上的安装步骤

### Windows  

1.需要本地安装Chrome且升级到最新正式版本  
  
2.安装python3  
  
[安装Python](https://www.python.org/downloads/)，一般选择最新版本的Python3及对应的Windows installer即可。安装时注意将为所有用户安装和将Python添加到PATH勾上
![安装python1](https://img.picgo.net/2022/08/07/1.png)
打开PowerShell，确认Python安装成功
![安装python2](https://img.picgo.net/2022/08/07/2.png)
  
3.安装`ffmpeg`，并确认安装正确  
  
- 下载安装`ffmpeg` & `ffprobe`：https://ffmpeg.org/download.html#build-windows  
- 将下载的`ffmpeg.exe`和`ffprobe.exe`路径添加到系统PATH  
- 在PowerShell确认ffmpeg和ffprobe安装成功  
  
4.安装`mktorrent`，并确认安装正确  

- 根据自己电脑下载[64位安装包](https://github.com/q3aql/mktorrent-win/releases/download/v1.1-2/mktorrent-1.1-win-64bit-build2.7z)或者[32位安装包](https://github.com/q3aql/mktorrent-win/releases/download/v1.1-2/mktorrent-1.1-win-32bit-build2.7z)  
- 使用[7-zip](http://www.7-zip.org/) or [Winrar](http://www.rarlab.com/)解压文件.  
- 将`mktorrent`文件夹移动到一个相对稳定的文件夹,比如`D:\Program Files\`  
- 将上一步`mktorrent\bin`文件夹路径添加到系统PATH 
我的电脑【右击】 -> 选择 属性 -> 高级系统设置 -> 高级 -> 环境变量  -> 系统变量里面找到'Path',点击编辑 -> 新建 -> 将上一步`mktorrent\bin`文件夹路径路径粘贴进去 -> 确定 --> 确定 … 保存即可。一般也是 不需要重启

5.安装`mediainfo`，并确认安装正确 
- 下载[mediainfo-cli](https://mediaarea.net/download/binary/mediainfo/22.06/MediaInfo_CLI_22.06_Windows_x64.zip)：https://mediaarea.net/en/MediaInfo/Download/Windows 
- 解压zip文件并解压后的`Mediainfo_CLIxxx`文件夹移动到一个相对稳定的位置
- 将上一步`Mediainfo_CLIxxx`文件夹路径添加到系统PATH  
我的电脑【右击】 -> 选择 属性 -> 高级系统设置 -> 高级 -> 环境变量  -> 系统变量里面找到'Path',点击编辑 -> 新建 -> 将上一步`Mediainfo_CLIxxx`文件夹路径粘贴进去 -> 确定 --> 确定 … 保存即可。一般也是 不需要重启。
- 在PowerShell确认`mediainfo`安装成功 
```
mediainfo -h
```

4.安装`Auto_Upload`，在以管理员身份打开`Windows PowerShell`中输入:
```
python3 -m pip install --upgrade auto_upload
auto_upload -h
```

### Linux
1.需要本地安装Chrome且升级到最新正式版本  
手动下载安装并更新即可，如果不方便手动，可以尝试使用如果命令（没有测试过） 
#### 安装Chrome  
``` bash
wget -q -O - [https://dl-ssl.google.com/linux/linux_signing_key.pub](https://dl-ssl.google.com/linux/linux_signing_key.pub) | sudo apt-key add -
sudo sh -c 'echo "deb [http://dl.google.com/linux/chrome/deb/](http://dl.google.com/linux/chrome/deb/) stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
```
#### 更新Chrome
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```
   
2.安装`mktorrent`,`ffmpeg`和`mediainfo`，并确认安装正确
```
sudo apt update && sudo apt install python3 python3-pip ffmpeg mediainfo mktorrent
```
  
3.安装`Auto_Upload`
```
python3 -m pip install --upgrade auto_upload
auto_upload -h
```

### MacOS
1.需要本地安装Chrome且升级到最新正式版本    
以Mac为例，2020.08.06最新正式版为104.0.5112.79  
  
2.安装`Homebrew`，在Termial.app中输入:
``` bash
bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
  
3.安装`mktorrent`,`ffmpeg`和`mediainfo`，并确认安装正确
```
brew install ffmpeg mediainfo mktorrent
ffmpeg -version
mediainfo --version
```
  
4.安装`Auto_Upload`，在`Terminal.app`中输入:
```
python3 -m pip install --upgrade auto_upload
auto_upload -h
```

## 配置环境&文件  

### 1.本地新建一个工作目录  
例如路径为:/Users/Desktop/auto_upload  

### 2.在1中工作路径文件夹下，再新建三个文件夹  
"cookies_path","screenshot_path","record_path"  

- cookies_path将用来存放站点cookie文件，文件名需要命名为cookie_站点.js。  
(例如:cookie_lemonhd.json,cookie_pter.json等)  
- screenshot_path将用来存放视频截图，种子等临时文件  
- record_path将用来存放发种记录 

### 3.获取cookie并存入文件 工作目录/cookies_path/cookie_站点.js 中  
js格式的cookie推荐使用插件"EditThisCookie"获取  

#### EditThisCookie插件官网  
http://www.editthiscookie.com/  

#### `Chrome`下`EditThisCookie`安装网址  
https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg  

#### `Edge`下`EditThisCookie`安装网址  
https://microsoftedge.microsoft.com/addons/detail/editthiscookie/jhampopgcdhehhkbeljdbfdbkfkmolbh?hl=zh-CN  

### 4.在文件夹中新建配置文件au.yaml
配置文件可以样例[au.yaml.example](https://github.com/dongshuyan/Auto_Upload/blob/main/au.yaml.example)填写 
详细参数说明参考[au_example.yaml](https://github.com/dongshuyan/Auto_Upload/blob/master/au_example.yaml)

建立完成后在工作目录下应该有三个文件夹以及一个au.yaml位置文件，如下图  
![Img_Demo](https://img.picgo.net/2022/08/06/dir.jpg)  


## 运行脚本
### 1.自动发种
``` bash
auto_upload -yp '工作目录/au.yaml' -u
```

### 2.本地图片自动上传图床
``` bash
auto_upload -yp '工作目录/au.yaml' -iu -ih 图床名称 -if  '图片路径1' '图片路径2'
```  
图床名称目前仅支持（排名无先后）：  
- ptpimg  
- picgo  
- chd  
- imgbox  
- pter  
- smms  

## 配置文件au.yaml详细说明  
参考 [au_example.yaml](https://github.com/dongshuyan/Auto_Upload/blob/master/au_example.yaml)  

## 常见错误及修复方法（更新ing）  

### Chrome未更新至最新  

## Reference
[Differential 差速器](https://github.com/LeiShi1313/Differential)  
[Differential差速器使用教程](https://leishi.io/blog/posts/2021-12/Differential/)  
[mktorrent-win-builds](https://github.com/q3aql/mktorrent-win-builds)  
[MKTORRENT WIN下命令行制作种子](https://blog.acesheep.com/index.php/archives/551/)  
[linux 安装 Chrome](https://www.cnblogs.com/ivantang/p/6290729.html)  
[windows10 环境变量设置](https://blog.csdn.net/palmer_kai/article/details/80588594)  

