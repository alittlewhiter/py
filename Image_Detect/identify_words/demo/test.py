# encoding:utf-8

import requests
import base64

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return base64.b64encode(fp.read())

# 使用baidu-aip库识别文本
img_src = 'result/0.jpg'
image = get_file_content(img_src)

# 使用HTTPS POST发送：https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=
mytoken = '24.eaca02598695fa4ed5aa8b8fbaed2517.2592000.1576573611.282335-17786614'
url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token='+mytoken;
headers = {'content-type':'application/x-www-form-urlencoded'}
params = {'image':image}

response = requests.post(url, data=params, headers=headers)
if response:
    print(response.json())
    print('图片识别结果为：\n')
    for result in response.json()['words_result']:
        print(result['words'])


