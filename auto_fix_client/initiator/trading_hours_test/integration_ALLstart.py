import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
'''
定义要遍历的文件夹列表
在本地调试是使用cgw101、cgw1022、cgw103，注意放到UAT环境要先确保clientGateway的状态是正常的，且无人使用       , 'cgw110'
'''
folders = ['cgw101', 'cgw102', 'cgw103', 'cgw104', 'cgw105', 'cgw106', 'cgw107', 'cgw108', 'cgw109']

# 创建新的Shell文件
with open('run_all.sh', 'w') as f:
    # 添加Shebang行，指定解释器为/bin/bash
    f.write('#!/bin/bash\n')

    # 存储要同时运行的Shell命令列表
    shell_commands = []


    # 遍历文件夹
    for folder in folders:
        # 获取文件夹中的文件列表
        files = os.listdir(folder)
        # 遍历文件列表
        for file in files:
            # 获取文件的绝对路径
            file_path = os.path.join(folder, file)
            # 判断文件类型为.sh
            if file.endswith('.sh'):
                # 添加执行.sh文件的命令
                shell_commands.append(['sh', file_path])
                f.write('sh ' + file_path + '\n')

# 添加执行权限给新的Shell文件
os.chmod('run_all.sh', 0o755)

# 同时运行所有脚本
with ThreadPoolExecutor() as executor:
    executor.map(subprocess.call, shell_commands)
