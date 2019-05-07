import requests
import json
import pytesseract
from PIL import Image, ImageDraw, ImageFilter


def removebg():
    #图片去底
    files = {'fileData': open('x.png', 'rb')}
    uploadimg = requests.post(url='http://www.aigei.com/tool/image/upload',files=files,headers=headers)
    img_url = json.loads(uploadimg.text)
    imgurl = img_url['fileUrl']
    ret_url = requests.get(url='http://www.aigei.com/bgremover/process?fileurl=%s&absvalue=80'%(imgurl),headers=headers)#容差80
    img_dataurl = json.loads(ret_url.text)
    imgdataurl = img_dataurl['fileUrl']
    r = requests.get(url='http://www.aigei.com/tool/image/visit/%s'%(imgdataurl),headers=headers)
    with open('img.png', 'wb') as f:
        f.write(r.content)

def analysis():
    imgName = 'img.png'
    im = Image.open(imgName)
    imgry = im.convert('L')
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    text = pytesseract.image_to_string(out)
    fomart = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for c in text:
        if not c in fomart:
            text = text.replace(c,'');
    text = text.lower()
    print("识别结果："+text)
    return text

def getimg():
    #带上cookie 防止不同步
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0','Cookie': 'PHPSESSID=khtfq3h72bgg6l06a5l5k1cl11'}
    r = requests.get(url='http://107.174.45.165/include/vdimgck.php',headers=header)
    with open('x.png', 'wb') as f:
        f.write(r.content)

def iftrue(text):
    global num
	#带上cookie 防止不同步
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0','Content-Type':'application/x-www-form-urlencoded','Cookie': 'PHPSESSID=khtfq3h72bgg6l06a5l5k1cl11'}
    data = 'gotopage=&dopost=login&adminstyle=newdedecms&userid=root&pwd=root&validate=%s&sm1='%(text)
    login = requests.post(url='http://107.174.45.165/dede/login.php',data=data,headers=header)
    if '验证码不正确' in login.text:
        print('\033[1;31m'+'[!]验证码不正确'+'\033[0m')
    else:
        print('\033[1;32m'+'[√]识别success'+'\033[0m')
        num = num + 1
        return num

if __name__ == '__main__':
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    global num
    num = 0
    for i in range(20):
        getimg()
        removebg()
        text = analysis()
        iftrue(text)
    print('[#]已识别20个验证码，在线检验成功%s个,成功率 %s %%'%(num,num/20*100))
