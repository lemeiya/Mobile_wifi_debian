# 随身WiFi刷Debian 部署ChatGPT

首先确定你手里的棒子是高通的CPU，此方法安装的是纯净版，安装好后4G内存的棒子还剩2.4G,不像别人做好的刷机包，他里面安装了很多东西，有些我们根本用不到，对于棒子内存小来说就是浪费资源。

## 第一、准备软件

> - 9008免签名驱动
> - MiKo (备份固件，以免成砖块)
> - 随身WiFi助手
> - Debian刷机包

## 第二、下载debian和base 包

1. **下载连接：https://github.com/OpenStick/OpenStick/releases/tag/v1**

![image-20230427213343857](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272133115.png)

2. **准备好定制的UFI003包。**

   **下载链接：https://www.123pan.com/s/XwVDVv-WICn3**

![image-20230427232804926](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272328971.png)

## 第三、备份固件

用miko备份，看我操作。

## 第四、整理包

1. UFI003_debian\UFI003\boot.img 复制到debian\boot.img（第一步下载的基础包）中进行替换。
2. 备份基带：我这里买的没有卡槽，我直接pass

## 第五、刷机

备份好之后把棒子拔下来，重新插上。

1. 进入fastboot模式，打开随身wifi助手，输入K
   ![image-20230427223033317](https://typeora.oss-cn-shenzhen.aliyuncs.com/img/202304272230381.png)
2. 先刷base包：进入base目录，点击flash.bat
3. 再刷debian包：进入debian目录，点击flash.bat

刷机完成后，把棒子拔下来，重新插拔。

## 第五、设置驱动和网络共享

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

## 第十二、安装docker

```shell
sudo curl -fsSL get.docker.com -o get-docker.sh `# 下载安装脚本` \
  && sudo sh get-docker.sh --mirror Aliyun `# 执行安装脚本` \
  && sudo systemctl enable docker `# 加入开机启动` \
  && sudo systemctl start docker `# 启动docker服务` \
  && sudo groupadd -f docker `# 创建docker组` \
  && sudo usermod -aG docker $USER `# 将当前用户加入docker组` \
  && sudo mkdir -p /etc/docker `# 创建配置目录` \
  && sudo newgrp docker `# 更新docker组信息`\
  && sudo echo -e '{\n  "registry-mirrors": ["https://fgyenivd.mirror.aliyuncs.com"]\n}' >> /etc/docker/daemon.json `# 设置阿里云镜像加速` \
  && sudo systemctl daemon-reload `# 重新加载所有系统服务配置` \
  && sudo systemctl restart docker `# 重启docker服务` \
  && sudo systemctl enable docker `# 开机启动 docker服务`
```

> 启动docker：sudo systemctl start docker
>
> 停止docker：sudo systemctl stop docker
>
> 重启docker：suto systemctl restart docker
>
> 开机启动docker：sudo systemctl enable docker
>
> 查看docker状态：sudo systemctl status docker
>
> 查看docker启动情况：docker version 
>
> 查看docker是否已经开机启动：sudo systemctl is-enabled docker

## 第十三、安装chatgpt

```shell
docker run -d -p 3000:3000 \
   -e OPENAI_API_KEY="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" \
   -e PROXY_URL="http://192.168.68.1:7890" \
   --restart=always \
   --name chatgpt-next-web \
   yidadaa/chatgpt-next-web
```

## 第十四、查看磁盘空间

安装了这么多软件后，我们来查看下磁盘空间：`df -h `

```shell
文件系统         容量  已用  可用 已用% 挂载点
udev             172M     0  172M    0% /dev
tmpfs             39M  1.4M   37M    4% /run
/dev/mmcblk0p14  3.3G  1.8G  1.4G   58% /
tmpfs            192M     0  192M    0% /dev/shm
tmpfs            5.0M     0  5.0M    0% /run/lock
tmpfs             39M     0   39M    0% /run/user/0
overlay          3.3G  1.8G  1.4G   58% /var/lib/docker/overlay2/f7427fb3224a325f67ab268819c56e4d36bd88dc37e7e8d3132450465b5873b7/merged
```

---

这是一个文件系统的磁盘空间使用情况报告，其中包括了多个挂载点的使用情况。具体解释如下：

- `/dev`：一个虚拟文件系统，用于表示设备节点，它的大小为 172M，当前没有占用空间。
- `/run`：一个临时文件系统，用于存储运行时需要的数据，例如进程ID等。它的大小为 39M，当前已经占用了 1.4M 的空间，剩余 37M。
- `/`：根文件系统，包含了操作系统和用户程序等文件，它的大小为 3.3G，已经使用了 1.8G，剩余可用空间为 1.4G，使用率为 58%。
- `/dev/shm`：一个虚拟文件系统，用于共享内存，它的大小为 192M，当前没有占用空间。
- `/run/lock`：一个临时文件系统，用于存储锁文件，它的大小为 5.0M，当前没有占用空间。
- `/run/user/0`：一个临时文件系统，用于存储当前用户在运行时创建的临时数据。它的大小为 39M，当前没有占用空间。
- `/var/lib/docker/overlay2/f7427fb3224a325f67ab268819c56e4d36bd88dc37e7e8d3132450465b5873b7/merged`: 其中的 `overlay` 是 Docker 容器所使用的联合文件系统，它的大小为 3.3G，已经使用了 1.8G，剩余可用空间为 1.4G，使用率为 58%。

比刷那些些定制版的省出很多空间哦

## 第十五、查看内存空间

执行：free -h

```shell
total        used        free      shared  buff/cache   available
内存：      382Mi       183Mi        36Mi       0.0Ki       161Mi       187Mi
交换：      191Mi        31Mi       159Mi
```

> 这是一份内存使用情况的统计报告，包括了物理内存和交换空间（Swap）的使用情况。根据该报告可以看出：
>
> - `total`：系统总共可用的内存大小为 382 MiB。
> - `used`：当前已经被占用的内存大小为 183 MiB。
> - `free`：当前未被占用的内存大小为 36 MiB。
> - `shared`：多个进程共享的内存大小为 0 KiB。
> - `buff/cache`：用于缓存磁盘数据的缓存区大小为 161 MiB。
> - `available`：还剩余可以分配的内存大小为 187 MiB。
>
> 而 `Swap` 则是交换空间的使用情况，包括了总大小、已经使用的大小和剩余可用空间大小：
>
> - `total`：总共可用的交换空间大小为 191 MiB。
> - `used`: 当前已经被占用的交换空间大小为 31 MiB。
> - `free`: 剩余可用的交换空间大小为 159 MiB。
>
> 需要注意的是，这里的内存大小单位为 MiB（兆字节），而非常见的 MB（百万字节）。
