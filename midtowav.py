import subprocess
import os
import shutil

folder_path = './trainset/classical/midfile'  # 文件夹路径
file_list = os.listdir(folder_path)  # 获取文件夹中的所有文件
for i in range(1):
    filename = str(i+1)
    savepath = folder_path+'/'
    # 定义要运行的命令
    command = ['FluidSynth', '-F', savepath + 'pianomusic' + filename + '.wav', './sf2/YDPGrandPiano20160804.sf2',
               savepath + 'pianomusic' + filename + '.mid']
    # 运行命令并等待其完成
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, error = process.communicate()
        if process.returncode != 0:
            print(f'An error occurred: {error}')
    print(str(i + 1))
# import os
# import shutil
#
# folder_path = './trainset/classical/midfile'  # 文件夹路径
# new_name_prefix = 'pianomusic'  # 新文件名前缀
#
# file_list = os.listdir(folder_path)  # 获取文件夹中的所有文件
#
# counter = 1  # 计数器，用于重命名文件
#
# for file_name in file_list:
#     if file_name.endswith('.mid'):  # 判断文件后缀是否为.mid
#         old_file_path = os.path.join(folder_path, file_name)  # 原文件路径
#         new_file_name = new_name_prefix + str(counter) + '.mid'  # 新文件名
#         new_file_path = os.path.join(folder_path, new_file_name)  # 新文件路径
#
#         shutil.move(old_file_path, new_file_path)  # 重命名文件
#
#         counter += 1  # 计数器加1