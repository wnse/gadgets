from tkinter import  *
from tkinter.filedialog import askdirectory
import shutil
import os
import re

def get_dir(path):
	dir_path = askdirectory()
	path.set(dir_path)

def copy_file(ori_dir, des_dir, pre, suf):
	if not pre and not suf:
		tmp = f'前缀 和 后缀 不能全为空'
		log_label.insert('end', f'{tmp:^70}\n')
		return None
	if not os.path.isdir(ori_dir):
		tmp = f'系统找不到指定的路径:{ori_dir}'
		log_label.insert('end', f'{tmp:^70}\n')
		return None
	if not os.path.isdir(des_dir):
		tmp = f'系统找不到指定的路径:{des_dir}'
		log_label.insert('end', f'{tmp:^70}\n')
		return None
	tmp = f'源文件夹路径: {ori_dir}'
	log_label.insert('end', f'\n{tmp:-^70}\n')
	tmp = f'目标文件夹路径: {des_dir}'
	log_label.insert('end', f'{tmp:-^70}\n')

	for i in os.listdir(ori_dir):
		f = os.path.join(ori_dir, i)
		if os.path.isdir(f):
			copy_file(f, des_dir, pre, suf)
		elif os.path.isfile(f):
			if re.match(pre, i) and re.search(f'{suf}$', i):
				des_file = os.path.join(des_dir, i)
				if os.path.isfile(des_file):
					log = f'{des_file} 已经存在'
				else:
					log = shutil.copy(f, os.path.join(des_dir, i))
					log = log + f' 拷贝成功'
				log_label.insert('end', f'{f} to {log}\n')
		else:
			log_label.insert('end', f'{f} 无法判断\n')

root = Tk()
root.title('copy files')

#### 图标
from icon import Icon
import base64
with open('tmp.ico','wb') as tmp:
    tmp.write(base64.b64decode(Icon().img))
root.iconbitmap('tmp.ico')
os.remove('tmp.ico')


help_info = (f'这个模块的作用是将源文件夹下\n所有与前缀和后缀匹配的所有文件（包括源文件夹下的文件夹）\n拷贝到目标文件夹下')
help_label = Label(root, text=f'{help_info:>1}', justify='left')
help_label.grid(row=0, columnspan=2)

path1=StringVar()
path1.set('源文件夹路径') 
path2=StringVar()
path2.set('目标文件夹路径') 

ori_label = Label(root, textvariable=path1)
ori_label.grid(row=1, column=1)
des_label = Label(root, textvariable=path2)
des_label.grid(row=2, column=1)

get_ori_b = Button(root, text='源文件夹路径', command=lambda: get_dir(path1))
get_ori_b.grid(row=1, column=0)
get_des_b = Button(root, text='目标文件夹路径', command=lambda: get_dir(path2))
get_des_b.grid(row=2, column=0)

pre_label = Label(root, text='前缀:')
pre_label.grid(row=3, column=0)
suf_label = Label(root, text='后缀:')
suf_label.grid(row=4, column=0)

pre_str = Entry(root, text='')
pre_str.grid(row=3, column=1)
suf_str = Entry(root, text='')
suf_str.grid(row=4, column=1)
copy_file_b = Button(root, text="开始拷贝", command=lambda: copy_file(path1.get(), path2.get(), pre_str.get(), suf_str.get()))
copy_file_b.grid(row=5)
log_label = Text(root)
log_label.grid(row=6, columnspan=2, sticky=W+E+N+S)
root.mainloop()
