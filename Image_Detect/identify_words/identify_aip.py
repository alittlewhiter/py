# encoding:utf-8

import os
import glob
import time
from os import path
from PIL import Image
from aip import AipOcr

# 调整图片大小，对于过大(>=4M)的图片进行压缩
def convert_image(img_src, out_dir):
    img = Image.open(img_src)
    width,height = img.size
    
    while (width*height > 4000000):
        width = width * 2 // 3
        height = height * 2 // 3
    new_img = img.resize((width, height), Image.BILINEAR)
    new_img.save(path.join(out_dir, os.path.basename(img_src)))

# 使用baidu-aip库识别文本
def ocr(img_src, results):
    filename = path.basename(img_src)
    img = open(img_src, 'rb')
    image = img.read()

    APP_ID = '17786614'
    API_KEY = 'aXuKPlGDGZ6c4T2ceXBlTkxZ'
    SECRET_KEY = 'id8pfEdwTuTdYrLFnAoM6LdChXi269CT'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    #client.setConnectionTimeoutInMillis(5000)

    print('正在识别图片：\t'+filename)
    options = {'language_type':'CHN_ENG'}
    message = client.basicGeneral(image, options)
    #message = client.basicAccurate(image)

    if message :
        print('识别图片成功！')
        with open(results, 'a+') as fp:
            fp.writelines('=' * 60 + '\n')
            fp.writelines('图片 '+filename+' : \n')
            for text in message.get('words_result'):
                fp.writelines(text.get('words') + '\n')
                #print(text)
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





