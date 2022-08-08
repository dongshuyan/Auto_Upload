## Auto_Upload  
自动将本地资源发布到PT站  
Upload local resources to PT trackers automatically.  

## 更新说明  
- 20220809 修复找不到bgm豆瓣链接的bug，增加识别发种dupe
- 20220808 增加qb添加种子稳定性、增加qb种子自动开始功能、增加后台运行的选项
添加考虑通过url下载站点种子失败的情况的判断  
增加qb种子自动开始功能、增加后台运行的选项参考 [au_example.yaml](https://github.com/dongshuyan/Auto_Upload/blob/master/au_example.yaml)
- 20220808 修复Windows系统上对于最终路径有空格等制作种子出错的bug。  
但是需要确保在制作种子期间，该`文件`或者`文件夹`没有被其他应用占用。仅对Windows系统有这个限制。  
  
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

### Windows(已测试成功)

1.需要本地安装Chrome且升级到最新正式版本  
  
2.安装python3  
  
[安装Python](https://www.python.org/downloads/)，一般选择最新版本的Python3及对应的Windows installer即可。安装时注意将为所有用户安装和将Python添加到PATH勾上
![安装python1](https://img.picgo.net/2022/08/07/1.png)
打开PowerShell，确认Python安装成功
![安装python2](https://img.picgo.net/2022/08/07/2.png)
  
3.安装`ffmpeg`，并确认安装正确  
  
- 下载安装`ffmpeg` & `ffprobe`：https://github.com/BtbN/FFmpeg-Builds/releases  
- 将解压后的`ffmpeg`文件夹移动到一个相对稳定的文件夹,比如`D:\Program Files\`  
- 将上一步`ffmpeg\bin`文件夹路径添加到系统PATH  
我的电脑【右击】 -> 选择 属性 -> 高级系统设置 -> 高级 -> 环境变量  -> 系统变量里面找到'Path',点击编辑 -> 新建 -> 将上一步`ffmpeg\bin`文件夹路径路径粘贴进去 -> 确定 --> 确定 … 保存即可。一般也是 不需要重启
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
python3 -m pip install auto_upload
auto_upload -h
```

### Linux  
0.升级`python`至`3.7.0`版本以上，建议`3.9.0`
如果有`_ssl`或者`_ctypes`找不到，也可以试试按照下面步骤重新安装python3
```bash
# 我也使用的wget ,我下载到了Download中
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
# 在home中解压
tar -zxf Python-3.9.0.tgz
# 进入python3.9
cd Python-3.9.0
 
# 编译文件  时间大概有1-3分钟
./configure --prefix=/usr/local/python3
 
# 编译好后，会有另外一个提示，让run ./configure xxx
./configure --enable-optimizations

# 安装pip依赖
sudo apt-get update
sudo apt-get install openssl
sudo apt-get install libssl-dev
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus
sudo apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev
sudo apt-get install zlib1g-dev libsqlite3-dev tk-dev
sudo apt-get install libssl-dev openssl
sudo apt-get install libffi-dev
sudo apt-get install libxpm-dev libxext-dev 
sudo apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev 

#配置ssl
./configure --with-ssl

# 给超级权限
sudo su

# 安装
make && make install

#退出超级权限
exit
 
# 结束
```

1.需要本地安装Chrome且升级到最新正式版本  
手动下载安装并更新即可，如果不方便手动，可以尝试使用如果命令（没有测试过） 
#### 安装Chrome  
``` bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
```
#### 更新Chrome
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```
   
2.安装`mktorrent`,`ffmpeg`和`mediainfo`，并确认安装正确
```bash
sudo apt update 
sudo python3 -m pip install --upgrade pip
sudo apt-get install python3-pip ffmpeg mediainfo mktorrent
```
  
3.安装`Auto_Upload`
```
python3 -m pip install auto_upload
auto_upload -h
```

### MacOS(已测试成功)
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
python3 -m pip install auto_upload
auto_upload -h
```

## 配置环境&文件  

### 1.本地新建一个工作目录  
例如路径为:/Users/Desktop/auto_upload  

### 2.在1中工作路径文件夹下，再新建三个文件夹  
"cookies_path","screenshot_path","m"  

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

- 安装好`EditThisCookie`之后
- 使用浏览器`成功登录`PT站点
- 点击右上角`饼干🍪`图案的图标
- 点击向右的按钮就把js格式的cookie复制的剪贴板了
- 粘贴进本文并保存到`工作目录/cookies_path/cookie_站点.js`文件即可

### 4.在文件夹中新建配置文件au.yaml
配置文件可以样例[au.yaml.example](https://github.com/dongshuyan/Auto_Upload/blob/main/au.yaml.example)填写 
详细参数说明参考[au_example.yaml](https://github.com/dongshuyan/Auto_Upload/blob/master/au_example.yaml)  
  
注意：如果是在windows系统下，要发布的`资源文件/文件夹名称`如果有`空格`会导致制作种子失败，建议将空格替换为`.`或者下划线`_`。其他系统没有这个问题。  
  
建立完成后在工作目录下应该有三个文件夹以及一个au.yaml位置文件，如下图  
![Img_Demo](https://img.picgo.net/2022/08/06/dir.jpg)  


## 运行脚本
### 1.自动发种
``` bash
auto_upload -yp '工作目录/au.yaml' -u
```
注意：在Windows系统发种时需要确保在制作种子期间，被发布的`文件`或者`文件夹`没有被其他应用占用。    
  
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
### Windows下 如果资源路径`最后的文件夹名称`有空格会导致制作种子失败（已修复）  
Windows下的mktorrent支持的不太好，后面我再修复吧  

## 交流群
群号:735803201

## Reference
[Differential 差速器](https://github.com/LeiShi1313/Differential)  (复制了上传图床部分代码)  
[Differential差速器使用教程](https://leishi.io/blog/posts/2021-12/Differential/)  (Auto_Upload安装教程主要参考本文)  
[mktorrent-win-builds](https://github.com/q3aql/mktorrent-win-builds)  
[MKTORRENT WIN下命令行制作种子](https://blog.acesheep.com/index.php/archives/551/)  
[linux 安装 Chrome](https://www.cnblogs.com/ivantang/p/6290729.html)  
[windows10 环境变量设置](https://blog.csdn.net/palmer_kai/article/details/80588594)  
[Linux Ubuntu系统升级Python3版本至Python3.9版本步骤](https://blog.csdn.net/u012080686/article/details/112600252)  
[PYTorrent](https://github.com/ndroi/pytorrent)
