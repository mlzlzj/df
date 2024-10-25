import requests
from urllib.parse import urlparse
from queue import Queue
import threading
import os
import time

# 定义下载速度阈值（单位：MB/s）
SPEED_THRESHOLD = 0.2


# 检测 URL 是否可用的 worker 函数
def check_url_available_worker(sources_queue: Queue, available_sources: list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    timeout = 5  # 设置超时时间

    while not sources_queue.empty():
        source = sources_queue.get_nowait()
        try:
            with requests.Session() as se:
                res = se.get(source['url'], headers=headers, timeout=timeout, stream=True)
                if res.status_code == 200:
                    # 计算下载速度
                    start_time = time.time()
                    total_bytes = 0
                    for content in res.iter_content(chunk_size=1 * 1024 * 1024):
                        total_bytes += len(content)
                        end_time = time.time()
                        duration = end_time - start_time
                        # 计算速度（字节/秒）
                        speed = total_bytes / duration if duration > 0 else 0
                        # 只测试下载第一个内容块
                        break
                    # 检查下载速度是否达到阈值
                    speed_mbs = speed / 1024 / 1024
                    if speed_mbs >= SPEED_THRESHOLD:
                        source['speed'] = speed_mbs  # 将下载速度添加到 source 字典中
                        available_sources.append(source)
                        print(
                            f"可用且速度达标 - {source['name']} - {source['url']} - 下载速度: {speed_mbs:.2f} MB/s")
                    else:
                        print(
                            f"速度未达标 - {source['name']} - {source['url']} - 下载速度: {speed_mbs:.2f} MB/s")
                else:
                    print(f"不可用 - {source['name']} - {source['url']}")
        except requests.exceptions.Timeout:
            print(f"请求超时 - {source['name']} - {source['url']}")
        except requests.exceptions.RequestException as ex:
            print(f"请求异常 - {source['name']} - {source['url']} - {ex}")
        except Exception as ex:
            print(f"出错 - {source['name']} - {source['url']} - {ex}")
        finally:
            sources_queue.task_done()


# 主函数，读取 iptv.txt，检测直播源，并写入 iptv_speed.txt
def check_and_write_iptv_speed_list():
    sources = []
    with open('iptv.txt', 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                sources.append({'name': parts[0], 'url': parts[1]})

    available_sources = []
    sources_queue = Queue()
    for source in sources:
        sources_queue.put(source)

    num_worker_threads = 100
    worker_threads = []

    for _ in range(num_worker_threads):
        t = threading.Thread(target=check_url_available_worker, args=(sources_queue, available_sources))
        t.start()
        worker_threads.append(t)

    sources_queue.join()

    for t in worker_threads:
        t.join()

    # 写入 iptv_speed.txt
    with open('iptv_speed1.txt', 'w', encoding='utf-8') as file:
        for source in available_sources:
            file.write(f"{source['name']},{source['url']} 下载速度 {source['speed']:.2f}M/s\n")

    print(f"检测完成，速度达标的可用直播源已写入 iptv_speed.txt")


# 运行主函数
if __name__ == "__main__":
    check_and_write_iptv_speed_list()
