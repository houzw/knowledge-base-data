#!/home/houzw/.conda/envs/gkb/bin/ python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/23 9:33
# execute this script on linux will raise no module names owlready2 error

from subprocess import run
import os, shutil

# for linux env
env_python = '/home/houzw/.conda/envs/gkb/bin/python'


# for windows without env
# env_python = 'python'
# run([env_python, './arcgis/demo.py'])

def generate():
	run([env_python, './taudem/taudem2owl_new.py'])
	run([env_python, './gdal/gdal2owl.py'])
	run([env_python, './saga/saga2owl.py'])
	run([env_python, './grass/grass2owl.py'])
	run([env_python, './arcgis/arc2owl.py'])
	run([env_python, './otb2owl/otb2owl.py'])
	run([env_python, './whitebox/whitebox2owl.py'])

# ok on windows not linux
# call('python ./taudem/taudem2owl_new.py')

# shutil.copyfile 需要第二个参数为完整的路径，包括文件名
# shutil.copy 第二个参数可以是目录
# move 要求目标文件不存在，即不支持覆盖已有文件
# download updated file 'task.owl' in './OwlConvert' manually
# generated file will be located in the same directory of this file

files = [{'file': 'taudem.owl', 'dir': './taudem'},
		 {'file': 'gdal.owl', 'dir': './gdal'},
         {'file': 'saga.owl', 'dir': './saga'},
         {'file': 'grass.owl', 'dir': './grass'},
         {'file': 'arcgis.owl', 'dir': './arcgis'},
         {'file': 'otb.owl', 'dir': './otb2owl'},
         {'file': 'whitebox.owl', 'dir': './whitebox'}]

def copy_to_directory(_files):
	for item in _files:
		shutil.copy(item['file'], item['dir'])  # 复制文件


def copy_to_statistic(_files):
	for item in _files:
		shutil.copy(item['file'], './Statistic')  # 复制文件


def remove_file(_files):
	for item in _files:
		os.remove(item['file'])


if __name__ == '__main__':
	generate()
	# copy first
	copy_to_directory(files)
	copy_to_statistic(files)
	remove_file(files)
	print('All done!')
