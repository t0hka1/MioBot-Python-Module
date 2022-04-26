import random
import requests
import uuid
import json
import time
from yiban import YiBan


def translate(word):
    url = 'https://fanyi.baidu.com/sug'
    data = {'kw': word}
    return str(json.loads(requests.post(url, data=data).text))


def getData(x_token, mode=0, week=7):
    # 获取当前时间戳
    timestamp = int(time.time() * 10000)
    getUrl = f'https://skl.hdu.edu.cn/api/paper/new?type={mode}&week={week}&startTime='.format(mode=mode,
                                                                                               week=week) + str(
        timestamp)  # 这里参数type中0为自测,1为考试。week参数为第几周。
    getHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Pragma': 'no-cache',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        # 获取当前uuid（测试发现是uuid1）
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        # 自己的token
        'X-Auth-Token': x_token
    }
    response = requests.get(getUrl, headers=getHeaders)
    return json.loads(response.text)


def postData(answer, x_token):
    url = 'https://skl.hdu.edu.cn/api/paper/save'

    postHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        'X-Auth-Token': x_token
    }
    requests.post(url, headers=postHeaders, data=answer)


def getAnswer(word):
    optionList = ['A', 'B', 'C', 'D']
    transResult = translate(word['title'])
    # print(transResult)
    for option in optionList:
        if word[f'answer{option}'] in transResult:
            return option
    for option in optionList:
        transResult = translate(word[f'answer{option}'])
        if word['title'] in transResult:
            return option

        if '，' in word['title']:  # 处理中文中的  （，）
            zhList = word['title'].split('，')
            if zhList[1] in transResult:
                return option
            elif zhList[0] in transResult:
                return option
        elif '......' in word['title']:  # 处理   (......)
            zhList = word['title'].split('...')
            if zhList[1] in transResult:
                return option
            elif zhList[0] in transResult:
                return option
    return 'C'


# if __name__ == '__main__':
def DoPaper():
    yb = YiBan("xxxx", "xxxx")  # FIXME:账号密码
    login = yb.login()
    X_Auth_Token = yb.auth()
    with open('answerList', 'r') as f:
        answerSource = f.read()
    answerDic = json.loads(answerSource) # 用于填充答案的文件
    paper = getData(X_Auth_Token, mode=1, week=7)  # FIXME:mode=0为自测,1为考试。week参数为第几周。
    print(paper)
    answerDic['paperId'] = paper['paperId']
    print('********正在答题中********')
    for index in range(0, 100):
        answerDic['list'][index]['input'] = getAnswer(paper['list'][index])
        answerDic['list'][index]['paperDetailId'] = paper['list'][index]['paperDetailId']
        print("第{}已答题".format(index))
    # 随机延时3-4分钟
    time.sleep(random.randint(180, 240))  # 测试时可关闭,正式使用时请打开
    postData(json.dumps(answerDic), X_Auth_Token)
    print('答题已结束')
    return "答题已结束"
