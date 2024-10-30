#coding:utf-8

import requests
import time

requests.packages.urllib3.disable_warnings()
result = []
RED = "\033[31m"
RESET = "\033[0m"
num = 0
with open("./test_domain.txt", "r") as f1:
    lines1 = len(f1.readlines())
    for line1 in f1.readlines():
        if line1.endswith("\n"):
            domain = line1[:-1]
        else:
            domain = line1
        with open("./vul_urlpath.txt","r") as f2:
            lines2 = len(f1.readlines())
            for line2 in f2.readlines():
                if line2.endswith("\n"):
                    url = "http://"+domain + line2[:-1]
                else:
                    url = "http://"+domain + line2
                try:
                    time.sleep(0.1)
                    # print(url)
                    r_precheck = requests.get(url = url, verify = False,timeout = 2)
                    num +=1
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
                    if num % 100 == 0: # "每完成100次扫描进行提醒"
                        print("扫描进度: ", num / line1*line2 * 100,"%")
                except Exception as err:
                    pass
                    # print(err)
print(result)
