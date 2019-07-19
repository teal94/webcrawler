import os
import sys

def get_list():
    f = open("data2.txt", "r", encoding='utf-8')
    str = f.read()
    f.close()
    return list(str.split('\n'))

list = get_list()

f = open("data2.txt", "w")
for e in list:
    line = e.split(':')[1]
    line = line.strip().split(',')[0]
    f.write(line+'\n')
f.close()

