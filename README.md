# holleworld网站
暂时没有想好到底做些什么，总之现在是一个练习的项目，锻炼自己从零搞起来一个web app！

## 增加了新闻模块
新闻模块支持显示，新建。新建的操作只能是管理员才能操作。（感觉权限统一继承一个类不好，但是还没
想到搞好的办法）TODO:支持markdown，但是语法不全：语法高亮等

## seassion和加密一系列工作
搞懂了tornado的log，之后写了一个父类，用于处理id的工作。还有就是seassion的管理

## tmplate模版
困死宝宝了！本来打算换模版引擎，把默认的换成JinJia2。后来发现好像有些麻烦，虽然实现没什么问题，
但是怕出现我控制不了的问题，暂时先这样。

现在准备抽象html，也就是在html中挖坑，然后方便以后的继承模版。

## 增加model层
因为打算完善功能，所以数据层的model是一定要做的。因为自己水平有限，所以就把廖雪峰老师写的model
层拿来用了。配置相关信息都发在config.py文件中，同时增加gitignore文件。


## 登陆功能
打算周末回家做好用户登录功能，就算做不完，也要做好数据库的工作。我一直很畏惧数据库的操作，事实
证明这种东西是躲不掉的！

## 部署网站
holleworld的部署方案本来原定是nginx＋supervisor。但是我发现tornado自带web服务器，同时
我现在又不要考虑并发问题。

所以今天我就直接没用nginx反向代理，直接启动脚本服务。然后用supervisor监视进程。
