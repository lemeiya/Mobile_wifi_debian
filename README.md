## 第一、刷机

备份好之后把棒子拔下来，重新插上。

1. 进入fastboot模式，打开随身wifi助手，输入K
   ![image-20230427223033317](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272230381.png)
2. 先刷base包：进入base目录，点击flash.bat
3. 再刷debian包：进入debian目录，点击flash.bat

刷机完成后，把棒子拔下来，重新插拔。

## 第二、设置驱动和网络共享

查看设备管理器中是否有NDIS，如果有直接跳过后面的操作，进入第五步。

![image-20230428111000644](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281110735.png)

![image-20230428111039495](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281110577.png)

---

这里会有一个驱动异常的rndis设备，右键，选择更新驱动，浏览我的电脑，以查找驱动程序

![image-20230428111940899](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281119967.png)

![image-20230428112110215](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281121286.png)

![image-20230428112132290](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281121364.png)

![image-20230428112153161](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281121236.png)

![image-20230428112203527](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281122596.png)

找到Microsoft，然后选择基于RNDIS网络共享设备（不同的系统可能不一样，但大同小异）。

![image-20230428112216090](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304281122177.png)

安装完驱动设备就可以被正常识别了，然后打开ssh（xshell、WindTerm等等都可以）。

## 第六、SSH登录

```shell
登录地址：ssh 192.168.68.1 

用户名：user 

密码：1
```

![image-20230427223256130](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272232193.png)

## 第七、设置root账户

```bash
#配置root用户密码 123456
sudo passwd root

#切换到root用户
sudo su -

#允许root用户远程登录，重启服务或系统后生效 
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

#重启设备
reboot

#用root设备登录ssh(密码是刚才设置的123456)
root---123456

#删掉已经没用的自带用户
userdel -r user
```



## 第八、连接网络

在终端输入`nmtui`，点击`Activate a connection`

![image-20230427224246380](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272242452.png)

![image-20230427224331397](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272243459.png)

![image-20230427224554796](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272245861.png)

在wifi名称前面带有*，就表示连接成功了。

![image-20230427224634036](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272246098.png)

## 第九、安装软件+设定镜像源

### a安装系统常用软件

```bash
#创建一个空mobian.list文件：
true > /etc/apt/sources.list.d/mobian.list

#更新APT软件包：
apt-get update


#安装常用的软件包
apt-get install curl
apt-get install -y wget
apt update
apt install vim git cron dnsutils unzip lrzsz fdisk gdisk exfat-fuse exfat-utils
```

### b设定阿里镜像源

```bash
#打开/etc/apt/sources.list文件
sudo vim /etc/apt/sources.list


#粘贴以下内容
deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb https://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main
deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
```

### c设定镜像后再次更新APT软件包

```
# 该命令会更新本地的软件包列表，会连接到远程软件源并检查可用的更新。
sudo apt update

# 这个命令会下载并安装系统中已经安装的软件包的最新版本，如果有新的依赖项则也会一并下载安装。
sudo apt-get upgrade
```

## 第十、配置系统时间

`dpkg-reconfigure tzdata` 选6.然后选70（亚洲 上海）

![image-20230427230735949](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272307023.png)

## 第十一、把Debian 设置中文环境

```
要支持区域设置，首先要安装locales软件包：
apt-get install locales

然后配置locales软件包：
dpkg-reconfigure locales

在界面中钩选487. zh_CN.UTF-8 UTF-8
输入487

然后输入3

#重启设备
reboot
```

![image-20230427231005088](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272310153.png)



设备重启后，再输入nmtui，就可以看到中文界面了：

![image-20230427231335786](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272313849.png)

