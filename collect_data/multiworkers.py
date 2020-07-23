import os
from multiprocessing import Pool
from collections import defaultdict, Counter

import json



CUR_DIR = os.path.dirname(os.path.abspath(__file__))

def sum_anchor_count(a, b):
    
    for key, value in b.items():
        a[key] += value
        
def multiworkers(func, task_list, save_file, workers=10):
    
    
    #writer_ptr = [open("{}{}".format(save_file, i), "w") for i in range(workers)]
    #worker_function = function_wrapper(func, writer_ptr)
    
    with open(save_file, "w") as outf:
        with Pool(workers) as p:
            for res in p.imap(func, task_list):
                print(*res, sep="\t", file=outf)
    #for ptr in writer_ptr:
    #    ptr.close()


def anchor_multiworkers(func, task_list, save_file, workers=10):
    
    
    #writer_ptr = [open("{}{}".format(save_file, i), "w") for i in range(workers)]
    #worker_function = function_wrapper(func, writer_ptr)
    anchor_count_total = defaultdict(Counter)
    count_total = 0
    
    with open(save_file, "w") as outf:
        with Pool(workers) as p:
            for res in p.imap(func, task_list):
                anchor_count_temp, count = res
                sum_anchor_count(anchor_count_total, anchor_count_temp)
                count_total += count
        print(count_total, file=outf)
        for key, value in anchor_count_total.items():
            print(key, json.dumps(value), sep="\t", file=outf)
    #for ptr in writer_ptr:
    #    ptr.close()

def test_func(value):
    
    return [value*value, 0]

if __name__ == "__main__":
    
    
    multi_workers(test_func, range(10), "tt")
        
        
