import calendar
import gzip
import os
import shutil
from datetime import datetime
import json
import warnings
from urllib.parse import unquote

import requests


def post_main(url, headers, data=None):
    warnings.filterwarnings("ignore")
    response = requests.post(url=url, headers=headers, data=data, verify=False)
    return response


# 通过传参控制所要登陆的环境
def login(env):
    sit_url = "https://adminui.sit.edp-atp.finstadiumxjp.com//api/admin/auth/login"
    uat_url = "https://adminui.uat.edp-atp.finstadiumxjp.com//api/admin/auth/login"
    data = json.dumps({
        "email": "xiang.chen@farsightedyu.com",
        "password": "ElevenChen123.",
        "verifyCode": "123"
    })
    headers = {
        "Content-Type": "application/json"
    }
    if env == 'SIT':
        response = post_main(sit_url, headers, data).json()
    elif env == 'UAT':
        response = post_main(uat_url, headers, data).json()
    else:
        return
    token_data = response['accessToken']
    access_token = "Bearer {}".format(token_data)
    return access_token


# 通过参数控制需要获取需要下载的文件名称
def get_date():
    # 获取当前时间
    date = datetime.now()
    day_year = date.year
    day_month = date.month
    day_day = date.day
    # # 如果是1号，则月份减1
    # if day_day == 1:
    #     day_month -= 1
    #     day_day = calendar.monthrange(day_year, day_month)[1]
    # else:
    #     day_day -= 1
    # 拼接时间字符串
    date_staring = f"{day_year}{day_month:02d}{day_day:02d}"
    return date_staring


# 保存下载的附件
def save_file(response, filename):
    # 获取当前目录路径
    current_dir = os.getcwd()
    # 创建 log 目录路径
    log_dir = os.path.join(current_dir, 'temp_file')
    # 确保 log 目录存在
    os.makedirs(log_dir, exist_ok=True)
    # 拼接文件路径
    file_path = os.path.join(log_dir, filename)

    # 将下载的内容写入文件
    with open(file_path, 'wb') as file:
        file.write(response.content)


# 解压压缩包
def decompress_gzip_file(input_path, output_dir):
    # 获取压缩文件的默认文件名
    base_filename = os.path.basename(input_path)
    # 去除文件扩展名
    base_filename = os.path.splitext(base_filename)[0]
    # 构建解压缩后的文件路径
    output_path = os.path.join(output_dir, base_filename)

    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('文件下载成功')


# EOD 下载请求
def download_eod(env, filename):
    print('文件下载中')
    # 定义两个环境url
    sit_url = "https://adminui.sit.edp-atp.finstadiumxjp.com//api/statistical-report/download-file"
    uat_url = "https://adminui.uat.edp-atp.finstadiumxjp.com//api/statistical-report/download-file"
    # 设计参数
    # 拼接EOD路径
    eod_file_path = "/data/RSec/for_RSec/EoD/EDP/{}_{}.csv.gz".format(filename,
                                                                      get_date())
    print('EOD文件路径：' + eod_file_path)
    data = json.dumps({
        "route": eod_file_path
    })
    # 构建请求头
    headers = {
        "Authorization": login(env),
        "Content-Type": "application/json"
    }
    # 判断环境SIT/UAT，如果不是直接return终止
    if env == 'SIT':
        response = post_main(sit_url, headers, data)
    elif env == 'UAT':
        response = post_main(uat_url, headers, data)
    else:
        return

    # 检查响应状态码，确认请求成功
    if response.status_code == 201:
        # 从响应中获取文件名
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1]
            filename = filename.strip('"')
            # 对获取到的文件名进行处理，去除引号问号空格及多余字符
            decoded_filename = unquote(filename)
            decoded_filename = decoded_filename.replace('"', '').strip('? ').rstrip()
        # 保存文件
        save_file(response, decoded_filename)
        # 定义压缩路径
        gz_file_path = 'temp_file/' + decoded_filename
        # 输出的解压缩文件目录
        output_dir = os.path.dirname(gz_file_path)
        # 解压缩文件
        decompress_gzip_file(gz_file_path, output_dir)
    else:
        # 处理请求失败的情况
        print('请求失败')
