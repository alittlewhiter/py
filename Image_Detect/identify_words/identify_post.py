# encoding:utf-8

import requests
import base64
import os
import glob
import time
from os import path
from PIL import Image


# 要求图像数据：base64编码后进行urlencode，去掉头部“ data:image/*;base64, ”字段
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return base64.b64encode(fp.read())

# 调整图片大小，对于过大(>=4M)的图片进行压缩
def convert_image(img_src, out_dir):
    img = Image.open(img_src)
    width,height = img.size
    
    while (width*height > 4000000):
        width = width * 2 // 3
        height = height * 2 // 3
    new_img = img.resize((width, height), Image.BILINEAR)
    new_img.save(path.join(out_dir, os.path.basename(img_src)))

''' client_id 为官网获取的AK，client_secret 为官网获取的SK
    注意access_token的有效期为30天，需要每30天进行定期更换
    此处token = '24.eaca02598695fa4ed5aa8b8fbaed2517.2592000.1576573611.282335-17786614'
'''
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=aXuKPlGDGZ6c4T2ceXBlTkxZ&client_secret=id8pfEdwTuTdYrLFnAoM6LdChXi269CT'
    response = requests.get(host)
    if response:
        #print(response.json())
        return response.json()['access_token']

mytoken = get_token()

# 使用Http请求响应方式调用baidu-aip
def ocr(img_src, results):
    filename = path.basename(img_src)
    image = get_file_content(img_src)

    # 使用HTTPS POST发送：https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token='+mytoken;
    headers = {'content-type':'application/x-www-form-urlencoded'}
    params = {'image':image}

    print('正在识别图片：\t'+filename)
    response = requests.post(url, data=params, headers=headers)
    if response:
        #print(response.json())
        print('图片 '+filename+' 识别成功！')
        with open(results, 'a+') as fp:
            fp.writelines('=' * 60 + '\n')
            fp.writelines('图片 '+filename+' : \n')
            for res in response.json()['words_result']:
                fp.writelines(res['words'] + '\n')
        print('\n')


if __name__ == '__main__':
    results = 'result/ocr_result.txt'
    tmp_dir = 'ocr_tmp'
    if not path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    if path.exists(results):
        os.remove(results)
        
    for img in glob.glob('result/*'):
        convert_image(img, tmp_dir)
    for img in glob.glob(tmp_dir+'/*'):
        ocr(img, results)
        time.sleep(3)

for img in glob.glob(tmp_dir+'/*'):
    os.remove(img)
os.removedirs(tmp_dir)




