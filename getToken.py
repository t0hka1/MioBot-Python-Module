from yiban import YiBan


def GetToken():
    yb = YiBan("xxxx", "xxxx")  # FIXME:账号密码
    login = yb.login()
    X_Auth_Token=yb.auth()
    return X_Auth_Token