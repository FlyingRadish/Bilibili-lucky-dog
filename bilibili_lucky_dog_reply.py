import requests
import json
import random
import itertools
import math

# 抽奖动态地址
link = 'https://t.bilibili.com/406122482490843947?tab=2'
# 通过开发者工具查到
oid = '406122482490843947'
reply_type = '17'

# 抽奖个数
count = 5
# 允许重复评论，允许填True，不允许填False
allow_duplicate = False

comments = []

def fetch_reply(page, reply_type, oid, referer):
    res = requests.get('https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn='+str(page)+'&type='+reply_type+'&oid='+oid+'&sort=2', headers={'referer':referer})
    data = json.loads(res.text)
    return data

def fetch_reply_reply(root, page, reply_type, oid, referer):
    res = requests.get('https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&ps=10&pn='+str(page)+'&type='+reply_type+'&oid='+oid+'&root='+root, headers={'referer':referer})
    data = json.loads(res.text)
    return data


print('抽奖动态地址：'+link)

# 获取第一页，计算之后的页数
data_in_first_page = fetch_reply(page=1, reply_type=reply_type, oid=oid, referer=link)['data']
max_page = math.ceil(data_in_first_page['page']['count'] / data_in_first_page['page']['size'])
declare_count = data_in_first_page['page']['acount']
print('共 '+str(max_page)+' 页, '+str(declare_count)+' 条评论')

for page in range(1,max_page+1):
    print('page '+str(page)+' loaded')
    data = fetch_reply(page=page, reply_type=reply_type, oid=oid, referer=link)['data']
    replies = data['replies']
    for reply in replies:
        user = {}
        user['ctime'] = reply['ctime']
        user['name'] = reply['member']['uname']
        user['mid'] = reply['member']['mid']
        user['space_link'] = 'https://space.bilibili.com/'+str(user['mid'])+'/dynamic'
        comments.append(user)
        # 处理楼中楼的情况
        if reply['rcount'] > 0:
            root_rpid = reply['rpid_str']
            child_data = fetch_reply_reply(root=root_rpid, page=1, reply_type=reply_type, oid=oid, referer=link)['data']
            child_max_page = math.ceil(child_data['page']['count'] / child_data['page']['size'])
            for child_page in range(1, child_max_page+1):
                child_data = fetch_reply_reply(root=root_rpid, page=child_page, reply_type=reply_type, oid=oid, referer=link)['data']
                child_replies = child_data['replies']
                if child_replies:
                    for child_reply in child_replies:
                        child_user = {}
                        child_user['ctime'] = child_reply['ctime']
                        child_user['name'] = child_reply['member']['uname']
                        child_user['mid'] = child_reply['member']['mid']
                        child_user['space_link'] = 'https://space.bilibili.com/'+str(child_user['mid'])+'/dynamic'
                        comments.append(child_user)

comments = sorted(comments, key=lambda item: item['ctime'])
result_size = len(comments)
print('result_count='+str(result_size))
if allow_duplicate:
    print('抽奖规则：抽 '+str(count)+' 人，按时间升序, 允许重复评论')
    print('评论总数：'+str(result_size))
else:
    mids = []
    filtered_comments = []
    for comment in comments:
        mid = comment['mid']
        if mid not in mids:
            mids.append(mid)
            filtered_comments.append(comment)
    comments = filtered_comments
    filtered_size = len(comments)
    print('抽奖规则：抽 '+str(count)+' 人，按时间升序, 不允许重复评论（取最早评论）')
    print('评论总数：'+str(result_size))
    print('去重后评论数：'+str(filtered_size))
for no in range(0,count):
    # 抽出来后就去掉，以免重复
    index = random.randint(0, len(comments)-1)
    lucky_dog = comments[index]
    print('第'+str(no+1)+'次：'+json.dumps(lucky_dog, ensure_ascii=False))
    comments.remove(lucky_dog)
