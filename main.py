import tkinter as tk
import time
import random as r
import numpy as np
from PIL import Image, ImageTk
# from bocchi import AnimatedGIFLabel

window = tk.Tk()
window.title("Number_random")
window.resizable(False,False)
window.geometry("1000x600")

# DjMist 水印
watermark = tk.Label(window,text="DjMist",fg="#c2c2c2")
watermark.pack(anchor="e")

# 小波奇
# animate_gif = AnimatedGIFLabel(window, "bocchi.gif", (200,200))
# animate_gif.place(x=0,y=400)

# 右边lab
lab1 = tk.Label(window,
        #   bg="#09ff00" # 显示lab
          ) # 选择学号进行抽签的lab
lab1.place(x=750,y=270)

# 左边lab
lab2 = tk.Label(window,
                # bg="#09ff00" # 显示lab
                ) # 设置学号范围进行抽取的lab
lab2.place(x=175,y=275)

# 范围设置
# 最小值
min = 1
min_var = tk.IntVar()
min_var.set(min)
text1 = tk.Label(lab2,text="最小值").grid(row=0)
ent1 = tk.Entry(lab2,textvariable=min_var)
ent1.grid(row=0,column=2)
# 最大值
max = 50
max_var = tk.IntVar()
max_var.set(max)
text2 = tk.Label(lab2,text="最大值").grid(row=1)
ent2 = tk.Entry(lab2,textvariable=max_var)
ent2.grid(row=1,column=2)
# 清除按钮
def clear_text():
    ent1.delete(0,tk.END)
    ent2.delete(0,tk.END)
    display.delete(0,tk.END)
clear = tk.Button(lab2,text="清除",command=clear_text)
clear.grid(row=3,column=0)
# 确认按钮
def check_min_max_func():
    global min,max,number_list,number_list_temp
    if ent1.get() != "" and ent2.get() != "":
        display.delete(0,tk.END)
        max = int(ent2.get())
        min = int(ent1.get())
        number_list = []
        number_list_temp = []
        for i in range(min,max+1):
            number_list.append(i)
            number_list_temp.append(i)
            display.insert(tk.END,number_list[i-1])
check_min_max = tk.Button(lab2,text="确认",command=check_min_max_func)
check_min_max.grid(row=3,column=1)

'''
选取学号进行抽签————————————————————————————————————————
'''
text3 = tk.Label(window,text="选取学号进行抽签",font=("宋体",20)).place(x=750,y=200)

number_list = []
number_list_temp = []

for i in range(min,max+1):
    number_list.append(i)
    number_list_temp.append(i)

def select_mode(): # 将用户输入的数字放入列表
    global number_list,number_list_temp
    number_list_temp = get_listbox_numbers()
    if select.get() != "": # 判定是否有输入
        number_list_temp.append(select.get())

    for i in range(len(number_list_temp)): # 将列表内的字符串转化为数值类型
        if min <= int(number_list_temp[i]) <= max:
            number_list_temp[i] = int(number_list_temp[i])
        else:
            number_list_temp.pop(i)
    select.delete(0,tk.END)

    number_list = np.sort(np.unique(number_list_temp)) # 查重排序
    display.delete(0,tk.END)
    for item in range(len(number_list)):
        display.insert(tk.END,number_list[item])

def select_mode_enter(temp): # 为bind而写
    select_mode()

select = tk.Spinbox(lab1,from_=min,to=max) # 数字输入框
select.bind("<Return>",select_mode_enter) # 回车检测
select.grid(row=1,column=1)

accpet = tk.Button(lab1,text="加入抽签列表",command=select_mode).grid(row=1,column=2) # 确认按钮

lab_1_1 = tk.Label(lab1,
                #    bg="#09ff00" # 显示lab
                   )
lab_1_1.grid(row=2,column=2)

# 删除列表中的学号
def get_listbox_numbers():
    numbers = [display.get(i) for i in range(display.size())]
    return numbers

def on_delete(): # 删除选中
    selected_indices = display.curselection()
    # 从后向前删除选中的元素，以防索引变化
    for i in reversed(selected_indices):
        display.delete(i)
delete_buttom = tk.Button(lab_1_1,text="删除学号",width=10,command=on_delete).grid(row=0,column=1)

def entry_delete(): # 删除输入的数字
    global number_list
    if delete.get() != "":
        for i in range(np.size(number_list)):
            try:
                if int(delete.get()) == number_list[i]:
                    number_list = np.delete(number_list,[i])
                    display.delete(i,i)
            except IndexError:
                pass
    delete.delete(0,tk.END)


def entry_delete_bind(temp): # 为bind
    entry_delete()

delete = tk.Spinbox(lab1,from_=min,to=max) # 数字输入框
delete.bind("<Return>",entry_delete_bind) # 回车检测
accpet_delete = tk.Button(lab1,text="剔除学号",width=10,command=entry_delete).grid(row=0,column=2)
delete.grid(row=0,column=1)

# 清空列表
def clear_list_func():
    global number_list_temp,number_list
    display.delete(0,tk.END)
    number_list = []
    number_list_temp = []
clear_list = tk.Button(lab_1_1,text="清空列表",width=10,command=clear_list_func).grid(row=1,column=1)


# 显示选取出来的学号列表
display = tk.Listbox(lab1)
display.grid(row=2,column=1)

for i in range(min,max+1):
    display.insert(tk.END,number_list[i-1])

'''
选取学号进行抽签————————————————————————————————————————
'''

# 抽取个数
text4 = tk.Label(window,text="抽取个数").place(x=445,y=340)
numbers_len = tk.Spinbox(window,from_=1,to=1000)
numbers_len.place(x=445,y=360)

# 抽签按钮
text_draw = "开始抽签"
final_numbers_list_add = []
final_numbers_list = []

def draw_func():
    global final_numbers_list,max
    final_numbers_list_add = [] # 临时列表
    if np.size(final_numbers_list) + int(numbers_len.get()) > max:
        return 0
    while np.size(final_numbers_list_add) < int(numbers_len.get()):
        if np.size(final_numbers_list) >= np.size(number_list):
            break
        r.seed(time.perf_counter()) 
        if ent1.get() != "" and ent2.get() != "":
            min = int(ent1.get())
            max = int(ent2.get())
            final_number = r.randint(min,max) # 随机数
            if final_number not in final_numbers_list and final_number in number_list:
                final_numbers_list_add.append(final_number) # 添加进列表
            tempList_1 = np.append(final_numbers_list_add,final_numbers_list)
            final_numbers_list_unique = np.unique(tempList_1)
            final_numbers_list = np.sort(final_numbers_list_unique) # 整理列表
            final_numbers_list_lab.configure(text=final_numbers_list)
        else:
            break

draw = tk.Button(window,text=text_draw,font=("宋体",40),command=draw_func).place(x=400,y=400)

# 显示抽取出来的学号
final_numbers_list_lab = tk.Label(window,text="等待抽取学号……",width=0,font=("宋体",20))
final_numbers_list_lab.place(x=0,y=10)
# 清空结果
def clear_numbers_func():
    global final_numbers_list
    final_numbers_list = []
    final_numbers_list_lab.configure(text="等待抽取学号……")

clear_numbers = tk.Button(window,text="清空结果",font=("宋体",15),command=clear_numbers_func)
clear_numbers.place(x=445,y=300)
window.mainloop()