# encoding:utf-8
# 
 
from urllib import request
import ssl
import json
import base64
import requests

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
host ='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=aXuKPlGDGZ6c4T2ceXBlTkxZ&client_secret=id8pfEdwTuTdYrLFnAoM6LdChXi269CT'

r = request.Request(host)
response = request.urlopen(r, context=gcontext).read().decode('UTF-8')
result = json.loads(response)
if (result):
    #print(result)
    mytoken = result['access_token']
    #print(token)

file = open('result/1.jpg', 'rb')
img = base64.b64encode(file.read())
