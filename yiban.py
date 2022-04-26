import json
import time
import base64
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def encryptPassword(pwd):
    # 密码加密
    PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
        Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
        XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
        KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
        A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
        AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
        d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
        7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
        mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
        AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
        uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
        ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
        -----END PUBLIC KEY-----'''
    cipher = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
    cipher_text = base64.b64encode(cipher.encrypt(bytes(pwd, encoding="utf8")))
    return cipher_text.decode("utf-8")


class YiBan:
    CSRF = "64b5c616dc98779ee59733e63de00dd5"  # 可随意填写
    COOKIES = {}
    HEADERS = {}
    location = ""

    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        self.session = requests.session()
        self.name = ""
        self.access_token = ""
        self.HEADERS = {"Origin": "'https://m.yiban.cn", 'AppVersion': '5.0.4', "User-Agent": "YiBan/5.0.4"}
        self.COOKIES = {"csrf_token": self.CSRF}

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            response = self.session.get(url=url, timeout=10, headers=self.HEADERS, params=params, cookies=cookies)
        else:
            response = self.session.post(url=url, timeout=10, headers=self.HEADERS, data=params, cookies=cookies)
        return response.json()

    def login(self):
        """
        登录
        :return:
        """
        params = {
            "mobile": self.mobile,
            "password": encryptPassword(self.password),
            "ct": "2",
            "identify": "0",
        }
        # 新的登录接口
        response = self.request("https://mobile.yiban.cn/api/v4/passport/login", method="post", params=params,
                                cookies=self.COOKIES)
        if response is not None and response["response"] == 100:
            self.access_token = response["data"]["access_token"]
            # print("login_token:" + self.access_token)
            self.HEADERS["Authorization"] = "Bearer " + self.access_token
            # 增加cookie
            self.COOKIES["loginToken"] = self.access_token
            print("login success!")
            return response
        else:
            return response


    # 接自己想搞的api来验证
    def auth(self):
        """
         易班内部上课啦小程序登录验证
         1.对https://f.yiban.cn/iapp/index?act=iapp319528发起请求
         发起的请求需装载(cookie:loginToken),User-Agent,loginToken,AppVersion
         拿到响应头里的Location
         2.对上面Location发起请求
         User-Agent,loginToken,AppVersion
         拿到响应头里的X-Auth-Token
         3.对https://skl.hdu.edu.cn/api/checkIn/code-check-in发起请求
         发起的请求需装载X-Auth-Token，User-Agent
         拿到json中的msg
         https://skl.hdu.edu.cn/api/checkIn/code-check-in?code=1423&latitude=30.319679101878627&longitude=120.33919365729693&t=163377400005
         """
        response = requests.get(url="https://f.yiban.cn/iapp/index?act=iapp319528",headers=self.HEADERS,cookies=self.COOKIES,allow_redirects=False)
        location = response.headers['Location']
        response = requests.get(url=location,headers=self.HEADERS,cookies=self.COOKIES,allow_redirects=False)
        X_Auth_Token = response.headers["X-Auth-Token"]
        print(X_Auth_Token)
        self.HEADERS["X-Auth-Token"] = X_Auth_Token
        return X_Auth_Token

