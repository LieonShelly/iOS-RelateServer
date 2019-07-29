# WCBServer

#### 环境配置
1. 拉取代码后，手动执行 source venv/bin/activate 激活虚拟环境
2. 执行 pip3 install -r requirements.txt 安装依赖包
3. 单机调试使用 flask run 命令运行程序 或者直接执行 python3 Run.py
4. 如果运行出现编码错误，依次执行 export LC_ALL=de_DE.utf-8，export LANG=de_DE.utf-8
5. 如果出现 Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.
    这种错误， 执行 export FLASK_APP=Run.py 

#### 注意事项
1. 所需的依赖包文件全部放在requirements.txt文件中
2. 文件或文件夹命名统一采用驼峰时命名
3. 代码其他规范参照官方文档 https://www.python.org/dev/peps/pep-0008/

### 测试服配置
1. ssh 登录 47.110.254.173  ZHONGchuan1014  (47.96.168.71(公))

2. 步进入虚拟环境

3. 运行screen

4. cd ~/PyEnvs

5. 创建项目web1 mkvirtualenv --python=/usr/local/Python-3.6.4/bin/python  web1

6. 切换虚拟环境：workon web1

7. 退出虚拟环境：deactivate

8. 列出所有环境：lsvirtualenv

9. 删除环境：rmvirtualenv [envname]

10. 显示环境详情：showvirtualenv [envname]

11. 赋值环境：cpvirtualenv [source] [dest]

12. 列出当前工作环境中安装的包：lssitepackages

13. 网站域名：www.scwcb.com


### 正式环境代码更新方法
 ssh 登录 47.96.168.71  ZHONGchuan1014

1.进入虚拟环境

  运行screen

2.切换虚拟环境：

 workon web1

cd /data/wwwroot/default

uwsgi --socket 127.0.0.1:3000 --enable-threads --master --processes 4 --threads 2 --py-autoreload=1 --home /root/PyEnvs/web1 --chdir /data/wwwroot/default --manage-script-name --mount /=Run:app

# 热更新
uwsgi --socket 127.0.0.1:3000 --enable-threads --master --processes 4 --threads 2 --py-autoreload=1 --home /root/PyEnvs/web1 --chdir /data/wwwroot/default --manage-script-name --mount /=Run:app

### 数据库admin
wanchebao  8mOUCcFMFpU3Jg1x


/ 

location /api/files {
      root    /data/wwwroot/default/Files
    }
    
location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|flv|mp4|ico)$ {
      expires 30d;
      access_log off;
    }

location ~ .*\.(bmp|swf|flv|mp4|ico)$ {
      expires 30d;
      access_log off;
    }

  