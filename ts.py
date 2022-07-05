import os
from pickle import FALSE, TRUE;

""" 
    1. 修改 user/src/bin/initproc.rs 第 11 行所执行的程序为 cs
         exec("cs\0", &[core::ptr::null::<u8>()]);

    2. 注意修改本脚本文件最终输出的原始数据文件名, 即本文件第 18 行

    3. 运行前需要确认测试文件 cost.rs 中的任务数量是否定义在本文件中 len_pos 所指定的位置

    4. 注意修改重复次数, 即本文件第 20 行

"""

file_name = './user/src/bin/cs.rs'
(pair_num_pos, len_pos) = (115, 118)
result_file_name = 'user_t_X.txt'
# 重复测试次数
REPEAT_NUM = 1

def set_args(pair_num, len):
    lines = []
    with open(file_name, 'r+') as f:
        lines = f.readlines()
        lines[pair_num_pos - 1] = str(pair_num) + '\n'
        lines[len_pos - 1] = str(len) + '\n'
    
    with open(file_name, 'w+') as f:
        f.write(''.join(lines))
    return



X = [2, 50, 100, 200, 400, 600, 800, 1000, 
    1200, 1400, 1600, 1800, 2000, 2200, 2400, 
    2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000]

Y = [200, 400, 600, 800, 1000, 1200, 1400, 
    1600, 1800, 2000, 2200, 2400, 2600, 2800, 
    3000, 3200, 3400, 3600, 3800, 4000]

text = ''

""" for x in X:
    for y in Y:
        if y >= x and y % x == 0:
            ok = FALSE
            while ok == FALSE:
                set_args(y/x, x)
                output = os.popen("python 1.py").read()

                output_lines = output.split("\n")
                for s in output_lines: 
                    line = s.split(' ')

                    if line[0] == '>>>':
                        print(str(x) + ' ' + str(y/x) + ' ' + line[1])
                        text = text + '\n# ' + str(x) + ' ' + str(y) + '\n' + line[1] + '\n'
                        ok = TRUE
                        break """


def calc_avg(arr):
    return sum(arr) / len(arr)

for x in X:
    for y in Y:
        if y >= x and y % x == 0:
            set_args(int(y/x), int(x))

            times = []

            while len(times) < REPEAT_NUM:
                ok = FALSE
                
                output = os.popen("cd os && make run").read()

                output_lines = output.split("\n")
                for s in output_lines: 
                    line = s.split(' ')
                    if line[0] == '>>>':
                        print(str(x) + ' ' + str(y/x) + ' ' + line[1])
                        #text = text + '\n# ' + str(x) + ' ' + str(y) + '\n' + line[1] + '\n'
                        ok = TRUE
                        break
                if ok == TRUE:
                    times.append(int(line[1]))

            text = text + '\n# ' + str(x) + ' ' + str(y) + '\n' + str(calc_avg(times)) + '\n'
            

text = text + '\n\n\n\n\n'
with open(result_file_name, 'w+') as f:
    f.write(text)