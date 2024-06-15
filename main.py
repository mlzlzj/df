import urllib.request
import re
import os
from datetime import datetime

# 定义要访问的多个URL
urls = [
    'https://raw.gitcode.com/ouu/scc/raw/main/kankan.txt',
    # 'https://taoiptv.com/source/iptv.txt?token=8zlxhttq9h01ahaw',
]

# 定义多个对象用于存储不同内容的行文本
ys_lines = []  # 央视频道
ws_lines = []  # 卫视频道
dy_lines = []  # 影视频道
hn_lines = []  # 地方台-湖南频道
sh_lines = []  # 地方台-上海频道
bj_lines = []  # 地方台-北京频道
sd_lines = []  # 地方台-山东频道
hb_lines = []  # 地方台-河北频道
zj_lines = []  # 地方台-浙江频道
ah_lines = []  # 地方台-安徽频道
hen_lines = []  # 地方台-河南频道
sx_lines = []  # 地方台-山西频道
sc_lines = []  # 地方台-四川频道
ln_lines = []  # 地方台-辽宁频道
hub_lines = []  # 地方台-湖北频道
gd_lines = []  # 地方台-广东频道
gx_lines = []  # 地方台-广西频道
js_lines = []  # 地方台-江苏频道
yn_lines = []  # 地方台-云南频道
cq_lines = []  # 地方台-重庆频道
jl_lines = []  # 地方台-吉林频道
xj_lines = []  # 地方台-新疆频道
gao_lines = []  # 地方台-港澳频道
tw_lines = []  # 地方台-台湾频道
radio_lines = []  # 地方台-地方电台
# other_lines = []


def process_name_string(input_str):
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str


def process_part(part_str):
    # 处理逻辑
    if "CCTV" in part_str and "://" not in part_str:
        # part_str = part_str.replace("IPV6", "")  # 先剔除IPV6字样
        part_str = part_str.replace("PLUS", "+")  # 替换
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():  # 处理特殊情况，如果发现没有找到频道数字返回原名称
            filtered_str = part_str.replace("CCTV", "")

        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):  # 特殊处理CCTV中部分4K和8K名称
            # 使用正则表达式替换，删除4K或8K后面的字符，并且保留4K或8K
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2:
                # 给4K或8K添加括号
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)

        return "CCTV" + filtered_str

    elif "卫视" in part_str:
        # 定义正则表达式模式，匹配“卫视”后面的内容
        pattern = r'卫视「.*」'
        # 使用sub函数替换匹配的内容为空字符串
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str

    return part_str


def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.request.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            channel_name = ""
            channel_address = ""

            # 逐行处理内容
            lines = text.split('\n')
            for line in lines:
                if "#genre#" not in line and "," in line and "://" in line:
                    channel_name = line.split(',')[0].strip()
                    channel_address = line.split(',')[1].strip()
                    # 根据行内容判断存入哪个对象
                    if "CCTV" in channel_name:  # 央视频道
                        ys_lines.append(process_name_string(line.strip()))
                    elif channel_name in ws_dictionary:  # 卫视频道
                        ws_lines.append(process_name_string(line.strip()))
                    elif channel_name in dy_dictionary:  # 影视频道
                        dy_lines.append(process_name_string(line.strip()))
                    elif channel_name in hn_dictionary:  # 地方台-湖南频道
                        hn_lines.append(process_name_string(line.strip()))
                    elif channel_name in sh_dictionary:  # 上海频道
                        sh_lines.append(process_name_string(line.strip()))
                    elif channel_name in bj_dictionary:  # 北京频道
                        bj_lines.append(process_name_string(line.strip()))
                    elif channel_name in sd_dictionary:  # 山东频道
                        sd_lines.append(process_name_string(line.strip()))
                    elif channel_name in hb_dictionary:  # 河北频道
                        hb_lines.append(process_name_string(line.strip()))
                    elif channel_name in zj_dictionary:  # 浙江频道
                        zj_lines.append(process_name_string(line.strip()))
                    elif channel_name in ah_dictionary:  # 安徽频道
                        ah_lines.append(process_name_string(line.strip()))
                    elif channel_name in hen_dictionary:  # 河南频道
                        hen_lines.append(process_name_string(line.strip()))
                    elif channel_name in sx_dictionary:  # 山西频道
                        sx_lines.append(process_name_string(line.strip()))
                    elif channel_name in sc_dictionary:  # 四川频道
                        sc_lines.append(process_name_string(line.strip()))
                    elif channel_name in ln_dictionary:  # 辽宁频道
                        ln_lines.append(process_name_string(line.strip()))
                    elif channel_name in hub_dictionary:  # 湖北频道
                        hub_lines.append(process_name_string(line.strip()))
                    elif channel_name in gd_dictionary:  # 广东频道
                        gd_lines.append(process_name_string(line.strip()))
                    elif channel_name in gx_dictionary:  # 广西频道
                        gx_lines.append(process_name_string(line.strip()))
                    elif channel_name in js_dictionary:  # 江苏频道
                        js_lines.append(process_name_string(line.strip()))
                    elif channel_name in yn_dictionary:  # 云南频道
                        yn_lines.append(process_name_string(line.strip()))
                    elif channel_name in cq_dictionary:  # 重庆频道
                        cq_lines.append(process_name_string(line.strip()))
                    elif channel_name in jl_dictionary:  # 地方台-吉林频道
                        jl_lines.append(process_name_string(line.strip()))
                    elif channel_name in xj_dictionary:  # 地方台-新疆频道
                        xj_lines.append(process_name_string(line.strip()))
                    elif channel_name in gao_dictionary:  # 港澳频道
                        gao_lines.append(process_name_string(line.strip()))
                    elif channel_name in tw_dictionary:  # 台湾频道
                        tw_lines.append(process_name_string(line.strip()))
                    elif channel_name in radio_dictionary:  # 地方台-地方电台
                        radio_lines.append(process_name_string(line.strip()))
                    # else:
                    #     other_lines.append(line.strip())


    except Exception as e:
        print(f"处理URL时发生错误：{e}")


current_directory = os.getcwd()  # 准备读取txt


# 读取文本方法
def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# 读取文本
ys_dictionary = read_txt_to_array('央视频道.txt')  # 仅排序用
ws_dictionary = read_txt_to_array('卫视频道.txt')  # 过滤+排序
dy_dictionary = read_txt_to_array('影视频道.txt')  # 过滤
hn_dictionary = read_txt_to_array('地方台/湖南频道.txt')  # 过滤
sh_dictionary = read_txt_to_array('地方台/上海频道.txt')  # 过滤
bj_dictionary = read_txt_to_array('地方台/北京频道.txt')  # 过滤
sd_dictionary = read_txt_to_array('地方台/山东频道.txt')  # 过滤
hb_dictionary = read_txt_to_array('地方台/河北频道.txt')  # 过滤
zj_dictionary = read_txt_to_array('地方台/浙江频道.txt')  # 过滤
ah_dictionary = read_txt_to_array('地方台/安徽频道.txt')  # 过滤
hen_dictionary = read_txt_to_array('地方台/河南频道.txt')  # 过滤
sx_dictionary = read_txt_to_array('地方台/山西频道.txt')  # 过滤
sc_dictionary = read_txt_to_array('地方台/四川频道.txt')  # 过滤
ln_dictionary = read_txt_to_array('地方台/辽宁频道.txt')  # 过滤
hub_dictionary = read_txt_to_array('地方台/湖北频道.txt')  # 过滤
gd_dictionary = read_txt_to_array('地方台/广东频道.txt')  # 过滤
gx_dictionary = read_txt_to_array('地方台/广西频道.txt')  # 过滤
js_dictionary = read_txt_to_array('地方台/江苏频道.txt')  # 过滤
yn_dictionary = read_txt_to_array('地方台/云南频道.txt')  # 过滤
cq_dictionary = read_txt_to_array('地方台/重庆频道.txt')  # 过滤
jl_dictionary = read_txt_to_array('地方台/吉林频道.txt')  # 过滤
xj_dictionary = read_txt_to_array('地方台/新疆频道.txt')  # 过滤
gao_dictionary = read_txt_to_array('地方台/港澳频道.txt')  # 过滤
tw_dictionary = read_txt_to_array('地方台/台湾频道.txt')  # 过滤
radio_dictionary = read_txt_to_array('地方台/地方电台.txt')  # 过滤


# 读取纠错频道名称方法
def load_corrections_name(filename):
    corrections = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            correct_name = parts[0]
            for name in parts[1:]:
                corrections[name] = correct_name
    return corrections


# 读取纠错文件
corrections_name = load_corrections_name('corrections_name.txt')


# 纠错频道名称
def correct_name_data(corrections, data):
    corrected_data = []
    for line in data:
        name, url = line.split(',', 1)
        if name in corrections and name != corrections[name]:
            name = corrections[name]
        corrected_data.append(f"{name},{url}")
    return corrected_data


def sort_data(order, data):
    # 创建一部字典来存储每行数据的索引
    order_dict = {name: i for i, name in enumerate(order)}

    # 定义一个排序键函数，处理不在 order_dict 中的字符串
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))

    # 按照 order 中的顺序对数据进行排序
    sorted_data = sorted(data, key=sort_key)
    return sorted_data


# 循环处理每个URL
for url in urls:
    print(f"处理URL: {url}")
    process_url(url)


# 定义一个函数，提取每行中逗号前面的数字部分作为排序的依据
def extract_number(s):
    num_str = s.split(',')[0].split('-')[1]  # 提取逗号前面的数字部分
    numbers = re.findall(r'\d+', num_str)  # 因为有+和K
    return int(numbers[-1]) if numbers else 999


# 定义一个自定义排序函数
def custom_sort(s):
    if "CCTV-4K" in s:
        return 2  # 将包含 "4K" 的字符串排在后面
    elif "CCTV-8K" in s:
        return 3  # 将包含 "8K" 的字符串排在后面 
    elif "(4K)" in s:
        return 1  # 将包含 " (4K)" 的字符串排在后面
    else:
        return 0  # 其他字符串保持原顺序


# 合并所有对象中的行文本（去重，排序后拼接）
version = datetime.now().strftime("%Y%m%d") + ",url"
all_lines = ["央视频道,#genre#"] + sort_data(ys_dictionary, set(correct_name_data(corrections_name, ys_lines))) + ['\n'] + \
            ["卫视频道,#genre#"] + sort_data(ws_dictionary, set(correct_name_data(corrections_name, ws_lines))) + ['\n'] + \
            ["影视频道,#genre#"] + sorted(set(correct_name_data(corrections_name, dy_lines))) + ['\n'] + \
            ["湖南频道,#genre#"] + sorted(set(correct_name_data(corrections_name, hn_lines))) + ['\n'] + \
            ["上海频道,#genre#"] + sort_data(sh_dictionary, set(correct_name_data(corrections_name, sh_lines))) + ['\n'] + \
            ["北京频道,#genre#"] + sort_data(bj_dictionary, set(correct_name_data(corrections_name, bj_lines))) + ['\n'] + \
            ["山东频道,#genre#"] + sort_data(sd_dictionary, set(correct_name_data(corrections_name, sd_lines))) + ['\n'] + \
            ["河北频道,#genre#"] + sort_data(hb_dictionary, set(correct_name_data(corrections_name, hb_lines))) + ['\n'] + \
            ["安徽频道,#genre#"] + sorted(set(correct_name_data(corrections_name, ah_lines))) + ['\n'] + \
            ["河南频道,#genre#"] + sorted(set(correct_name_data(corrections_name, hen_lines))) + ['\n'] + \
            ["浙江频道,#genre#"] + sorted(set(correct_name_data(corrections_name, zj_lines))) + ['\n'] + \
            ["山西频道,#genre#"] + sorted(set(correct_name_data(corrections_name, sx_lines))) + ['\n'] + \
            ["四川频道,#genre#"] + sorted(set(correct_name_data(corrections_name, sc_lines))) + ['\n'] + \
            ["辽宁频道,#genre#"] + sorted(set(correct_name_data(corrections_name, ln_lines))) + ['\n'] + \
            ["湖北频道,#genre#"] + sorted(set(correct_name_data(corrections_name, hub_lines))) + ['\n'] + \
            ["广东频道,#genre#"] + sorted(set(correct_name_data(corrections_name, gd_lines))) + ['\n'] + \
            ["广西频道,#genre#"] + sorted(set(correct_name_data(corrections_name, gx_lines))) + ['\n'] + \
            ["江苏频道,#genre#"] + sorted(set(correct_name_data(corrections_name, js_lines))) + ['\n'] + \
            ["云南频道,#genre#"] + sorted(set(correct_name_data(corrections_name, yn_lines))) + ['\n'] + \
            ["重庆频道,#genre#"] + sorted(set(correct_name_data(corrections_name, cq_lines))) + ['\n'] + \
            ["吉林频道,#genre#"] + sorted(set(correct_name_data(corrections_name, jl_lines))) + ['\n'] + \
            ["新疆频道,#genre#"] + sorted(set(correct_name_data(corrections_name, xj_lines))) + ['\n'] + \
            ["港澳频道,#genre#"] + sort_data(gao_dictionary, set(correct_name_data(corrections_name, gao_lines))) + ['\n'] + \
            ["台湾频道,#genre#"] + sort_data(tw_dictionary, set(correct_name_data(corrections_name, tw_lines))) + ['\n'] + \
            ["地方电台,#genre#"] + sort_data(radio_dictionary, set(radio_lines)) + ['\n'] + \
            ["更新时间,#genre#"] + [version]

# 将合并后的文本写入文件
output_file = "iptv_list.txt"
# others_file = "qita.txt"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

    # with open(others_file, 'w', encoding='utf-8') as f:
    #     for line in other_lines:
    #         f.write(line + '\n')
    # print(f"其他文件已保存到文件: {others_file}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")

