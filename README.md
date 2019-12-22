### linux_python_exporter

#### 配置python包
```
pip2 install -i http://mirrors.aliyun.com/pypi/simple/  psutil
pip2 install -i http://mirrors.aliyun.com/pypi/simple/ prometheus_client
```
#### 修改Prometheus监听端口
Prometheus会周期遍历exporter，代码中设置exporter端口是`9999`，所以要修改Prometheus的配置端口为`9999`，即可启动`linux_python_exporter`，启动Prometheus，即可上传监控数据。

#### 目前实现功能
* cpu监控
* mem监控
* 网络io监控
* 磁盘使用量监控
* 磁盘io监控
