from iLoveWord import *
from getToken import *
from flask import *

app=Flask(__name__)

# 获取上课啦小程序的token
@app.route('/token')   
def getToken():
    return GetToken()

# 完成我爱记单词
@app.route('/word')
def iLoveWord():
    return DoPaper()


if __name__ == '__main__':
    app.run()

