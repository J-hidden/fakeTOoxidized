

# 仿写Oxidized

## 前言

​	书接上一篇文章介绍了自动化备份网络设备的开源工具oxidized。不可否认的是这个工具用起来挺好，但是对我来说还是有如下几个缺点。

1. 软件通过Ruby编写，遇见问题无法解决。不了解Ruby
2. 华为的防火墙设备好像不支持
3. 实在不知道类似于锐捷、juniper或者其他厂商的model是什么

​	但是优点也很明显

* 简单大气的WEB界面，一目了然的看出哪些设备备份了，哪些是有改动配置的
* 循环自动化备份，而且支持多进程
* 安装简单，日志记录比较详细

综上所述，我希望能够写出一份基于python的Oxidized,可以实现其大部分功能，但是UI界面就将就一些。有兴趣的同学可以后期更改

## 正文

###  Linux操作步骤

#### 前置条件 

* Linux需要安装python3.6+
* 安装wget
* 安装模块 virtualenv模块

1. git clone https://github.com/J-hidden/fakeTOoxidized.git

![image-20220114145220102](/Users/lixilei/Library/Application Support/typora-user-images/image-20220114145220102.png)

2. 进入文件夹，建立虚拟环境文件夹且进入虚拟环境

![image-20220114145912552](/Users/lixilei/Library/Application Support/typora-user-images/image-20220114145912552.png)

注意：进入虚拟环境时命令最前方会有（venv）标识

![image-20220114145939101](/Users/lixilei/Library/Application Support/typora-user-images/image-20220114145939101.png)

3、安装required.txt文件中对应模块

* 首先我们先更新一下pip,通过在最后加```-i http://pypi.douban.com/simple --trusted-host pypi.douban.com``可以将更新源指向国内，这样就不会出现timeout情况
* 如果不好用可以用以下的几种

> pypi 清华大学源：[https://pypi.tuna.tsinghua.edu.cn/simple](https://link.zhihu.com/?target=https%3A//pypi.tuna.tsinghua.edu.cn/simple)
> pypi 豆瓣源 ：[http://pypi.douban.com/simple/](https://link.zhihu.com/?target=http%3A//pypi.douban.com/simple/)
> pypi 腾讯源：[http://mirrors.cloud.tencent.com/pypi/simple](https://link.zhihu.com/?target=http%3A//mirrors.cloud.tencent.com/pypi/simple)
> pypi 阿里源：[https://mirrors.aliyun.com/pypi](https://link.zhihu.com/?target=https%3A//mirrors.aliyun.com/pypi/simple/)

```python
pip install 模块名 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114161821969.png" alt="image-20220114161821969" style="zoom:50%;" />

* 通过命令  ```pip3 install -r requeired.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com```安装其模块。

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114162254936.png" alt="image-20220114162254936" style="zoom:50%;" />

* 然后就可以通过python启动项目了。

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114162434888.png" alt="image-20220114162434888" style="zoom:50%;" />

但是我反复安装都发现Django和django-simpleui都无法一起安装上。所以我们需要手动安装

这是因为我写的时候使用的虚拟环境，无法上传到github.所以虚拟环境需要大家自行安装。下面是我列举的需要用到所有第三方模块

* Django
* Django_simpleui
* netmiko
* schedule
* difflib(这个好像是内置的)

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114163325149.png" alt="image-20220114163325149" style="zoom:50%;" />

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114163412857.png" alt="image-20220114163412857" style="zoom:50%;" />

然后再启动项目：

PS：这中间会有同学会遇到如下问题。可[点击此处解决](https://blog.csdn.net/weixin_42167759/article/details/90648225)。我使用的是第二种方案解决

![image-20220114163550913](/Users/lixilei/Library/Application Support/typora-user-images/image-20220114163550913.png)

然后便是启动成功。启动成功后先别急。先重置一下数据库，这样子才可以登入到后台页面。

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114163919673.png" alt="image-20220114163919673" style="zoom:50%;" />

然后创建登入后台的账号：

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114163959686.png" alt="image-20220114163959686" style="zoom:50%;" />

* 打开 ``http:IP:60258/admin``界面

![image-20220114164118040](/Users/lixilei/Library/Application Support/typora-user-images/image-20220114164118040.png)

登入进去后Device是设备组。可以增加设备。按照对应要求添加即可。其中设备类型填写netmiko的device_type即可

![image-20220114164210649](/Users/lixilei/Library/Application Support/typora-user-images/image-20220114164210649.png)

然后运行 oxidized/coll.py文件即可定期采集配置并且进行对比。

* 运行注意事项

 可以打开两个终端用来调试

一个用于运行 python3 manage.py runserver 0.0.0.0:60258

一个用来运行  python3 oxidized/coll.py

### 

* 采集完成后，差异信息如下所示：

1. 上面的***xx,xx**** 是之前的配置，后面的 ---xx, xxx---是现在配置。总体来说就是更改了哪些配置
2. ！ 是这一行做了改动

具体可以看一下difflib函数的使用说明

```tex
*** 

--- 

***************

*** 67,73 ****

   mad detect mode relay
  #
  interface GigabitEthernet0/0/1
!  description abc
   port link-type trunk
   port trunk allow-pass vlan 2 to 4094
  #
--- 67,73 ----

   mad detect mode relay
  #
  interface GigabitEthernet0/0/1
!  description test1
   port link-type trunk
   port trunk allow-pass vlan 2 to 4094
  #
```

## 自定义

基本上所有代码都在oxidized/coll.py 下，所需要更改的也基本上都是coll.py

###  一、添加原生不支持设备

​	在  oxidized/coll.py 中35-42行有如下代码。添加格式为：

```python
elif platform == '此处填写netmiko的device_type':
                output = conn.send_command('此处填写查看运行配置的命令')
```

<img src="/Users/lixilei/Library/Application Support/typora-user-images/image-20220114164652458.png" alt="image-20220114164652458" style="zoom:50%;" />

需要注意的是要上下对齐

### 二、更改采集设备配置的间隔时间

​	同样是在 oxidized/coll.py中第96-101行中

```python
def task_list():
    schedule.clear()
    schedule.every(60).seconds.do(backup_config) #此处为间隔时间
    while True:
        schedule.run_pending()
        time.sleep(30)   # 此处为采集完成后间隔多长时间再次执行采集动作
```

