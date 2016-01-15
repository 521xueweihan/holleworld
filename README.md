# holleworld网站
holleworld的部署方案本来原定是nginx＋supervisor。但是我发现tornado自带web服务器，同时
我现在又不要考虑并发问题。

所以今天我就直接没用nginx反向代理，直接启动脚本服务。然后用supervisor监视进程。

## TODO:
打算周末回家做好用户登录功能，就算做不完，也要做好数据库的工作。我一直很畏惧数据库的操作，事实
证明这种东西是躲不掉的！
