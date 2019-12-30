# -*- coding: utf-8 -*-

import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = ''  #企业ID，在管理后台获取
        self.CORPSECRET = ''#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000002'  #应用ID，在后台应用中获取
        self.TOUSER = "HuangJianBin"  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        access_token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={ID}&corpsecret={SECRET}'.format(ID=self.CORPID,SECRET=self.CORPSECRET)
        response = requests.get(access_token_url)
        data = json.loads(response.text)
        return data['access_token']

    def get_access_token(self):  #因为凭证的有效时间是2个小时，所以要判断上一个凭证是否还有效
        try:
            with open('/Users/lol/Desktop/access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:#如果有异常
            with open('/Users/lol/Desktop/access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else: #如果没有异常
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7200:
                return access_token
            else:
                with open('/Users/lol/Desktop/access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        access_token = self.get_access_token()
        send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'.format(token=access_token)
        send_values = {
            "touser" : self.TOUSER,
            "msgtype" : "text",
            "agentid" : 1000002,
            "text" : {
                "content" : message
            },
            "safe":0
        }
        send_response = requests.post(url=send_msg_url,data=json.dumps(send_values))        
        send_response = send_response.json()   #当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return send_response["errmsg"]


if __name__ == '__main__':
    wx = WeChat()
    wx.send_data("whoami111")