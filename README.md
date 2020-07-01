# Bilibili-lucky-dog
一个B站抽奖脚本

**本脚本仅供研究实验，不对其运行产生的结果负任何责任**

## 这个脚本能做什么？
当然是抽奖，可以抓取当前某个动态下所有的评论(划重点)来抽取幸运儿。

## 可选配置
1. 抽奖个数
2. 是否去重

## 食用指南
1. 安装python3
2. 命令行输入`pip install requests`安装requests网络请求库
3. 配置好各项参数后(详见下文)，命令行下运行`python bilibili_lucky_dog_reply.py`即可

### oid、reply_type的获取方式
1. 打开要抽奖的动态详情页
2. 打开浏览器开发者工具
3. 按F5刷新
依照图示找到oid、reply_type，填入脚本中
![Example](https://github.com/houxg/Bilibili-lucky-dog/blob/master/example1.png)
