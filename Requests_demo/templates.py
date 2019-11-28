
import requests

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=100)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(r.status_code)
        return "连接产生异常"

if __name__ == "__main__":
    url = "https://www.bilibili.com"
    print(getHTMLText(url))

print("\nEnd.")
