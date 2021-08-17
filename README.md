<!--
 * @Description: 
 * @Version: 1.0
 * @Autor: Tu Ruwei
 * @Date: 2021-07-13 18:10:32
 * @LastEditors: Tu Ruwei
 * @LastEditTime: 2021-08-17 10:50:42
-->

## KVManager

### Ubuntu

#### 1.安装mysql

```shell
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient-dev
# 查看是否安装成功
netstat -tap | grep mysql
# 安装验证密码插件。 N 输入密码 Y N Y Y 
mysql_secure_installation
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
#注释掉bind-address = 127.0.0.1
# 进入数据库 8.0版本
mysql> create user root@'%' identified by '123456';
mysql> grant all privileges on *.* to root@'%' with grant option;
# 8.0版本之前
mysql> grant all on *.* to root@'%' identified by '你的密码' with grant option;
mysql> flush privileges;
sudo systemctl enable mysql
sudo systemctl restart mysql
```

#### 2.安装redis

```shell
# 自行安装，注意配置密码
```



#### 3.安装依赖

```shell
sudo apt-get -y install git virtualenv python3-virtualenv python3-dev python3-lxml libvirt-dev zlib1g-dev libxml2-dev libxslt1-dev nginx libsasl2-modules gcc pkg-config python3-guestfs libsasl2-dev libldap2-dev libssl-dev nodejs npm --fix-missing
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn
sudo systemctl enable nginx
sudo systemctl restart nginx
git clone https://github.com/tmooming/KVManager.git
cd 
```

#### 4. 配置

```shell
cd KVManager
vitualenv env
source env/bin/activate
cd client
# 修改后端地址
vim src/utils/cors-requests.js
yarn install
yarn run build:prod
cd ../server
pip install -r requirments.txt
# 将地址改成本机IP
vim kvmanager.conf
vim gconfig.py
# 根据需求，修改镜像上传模块地址
vim resources/kvm/instance.py
cp kvmanager.conf /etc/nginx/conf.d/
cp kvmanager.service /etc/systemd/system/
cp gunicorn /etc/logrotate.d/
sudo systemctl daemon-reload
sudo nginx -s reload
sudo cp -r ../KVManager /srv/
sudo chown -R www-data:www-data /srv/KVManager
sudo systemctl start kvmanager

```

#### 4.完成

登录页面即可
