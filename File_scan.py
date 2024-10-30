#coding:utf-8

import requests
import time

requests.packages.urllib3.disable_warnings()


# http_proxy = 'http://10.0.22.164:8080'
# https_proxy = 'https://10.0.22.164:8080'

# # 创建一个字典，包含代理信息
# proxies = {
#     'http': http_proxy,
#     'https': https_proxy,
# }

result = []
RED = "\033[31m"
RESET = "\033[0m"
with open("./test_domain.txt", "r") as f1:
    for line1 in f1.readlines():
        if line1.endswith("\n"):
            domain = line1[:-1]
        else:
            domain = line1
        with open("./vul_urlpath.txt","r") as f2:
            for line2 in f2.readlines():
                if line2.endswith("\n"):
                    url = "http://"+domain + line2[:-1]
                else:
                    url = "http://"+domain + line2
                try:
                    time.sleep(0.1)
                    # print(url)
                    r_precheck = requests.get(url = url, verify = False,timeout = 2)
                    # print(url,r_precheck.status_code)
                    if r_precheck.status_code == 200:
                        time.sleep(0.5)
                        # print(url)
                        r_real_eists_check = requests.get(url = url + "yTRejwjP_875", verify = False,timeout = 2)
                        # print(len(r_precheck.text))
                        # print(len(r_real_eists_check.text))
                        if r_real_eists_check.status_code == 200:
                            if len(r_precheck.text) == len(r_real_eists_check.text) or len(r_real_eists_check.text) - len(r_precheck.text) == 12:
                            # print("误报")
                                pass
                            else:
                                result.append(url)
                                # print(url,r_precheck.status_code)
                                print(RED,url+"  真实存在",RESET)
                except Exception as err:
                    pass
                    # print(err)
print(result)
