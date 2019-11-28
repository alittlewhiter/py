#简单图片爬取 代码模板
import requests
import os

url = 'https://edu-image.nosdn.127.net/3321D6673EB82C94D08E1B80E8344166.jpg'
save = 'F://get_imgs//'
path = save+url.split('/')[-1]
try:
    if not os.path.exists(save):
        os.mkdir(save)
    if not os.path.exists(path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print("图片爬取成功")
    else:
        print('文件已存在')
except:
    print('图片爬取失败')

print('\nEnd.')



