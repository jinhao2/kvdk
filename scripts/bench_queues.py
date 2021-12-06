import os
import datetime
import git
import sys
from select import select

n_thread = 64
sz_value = 120                          
t_duration = 30                         
populate_if_fill = 1   
sz_pmem_file = 384 * 1024 * 1024 * 1024 
sz_fill_data = 96 * 1024 * 1024 * 1024
n_collection = 16

path_pmem = "/mnt/pmem0/kvdk_queue"

numanode = 0
bin = "../build/bench"
exec = "numactl --cpunodebind={0} --membind={0} {1}".format(numanode, bin)


def Confirm(dir):
    timeout = 60
    print("Instance path : {}, it will be removed and recreated, confirm? (y/n) (Automatically confirm in 60 seconds)".format(path_pmem))
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    y = 'n'
    if rlist:
        y = sys.stdin.readline(1)
    else:
        print("Automatically confirmed after 60 seconds!")
        y = 'y'
    if y != 'y':
        exit(1)

def run_bench_mark(
    n_thread=n_thread,
    sz_value=sz_value, 
    t_duration=t_duration, 
    populate_if_fill=populate_if_fill,
    sz_pmem_file=sz_pmem_file, 
    sz_fill_data=sz_fill_data,
    n_collection=n_collection,
    path_pmem=path_pmem):

    n_thread_total = n_thread
    n_thread_write = n_thread
    git_hash = git.Repo(search_parent_directories=True).head.object.hexsha
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    sz_key = 8                              # Not configuarble for now

    path_report = "./results-queue-threads-{}-key-{}-value-{}-collections-{}-timestamp-{}-commit-{}/".format(
        n_thread, 
        sz_key,
        sz_value,
        n_collection,
        timestamp,
        git_hash)

    Confirm(path_pmem)
    os.system("rm -rf {0}".format(path_pmem))

    os.system("mkdir -p {}".format(path_report))
    n_operations = sz_fill_data // (sz_value + sz_key)
    para_shared = "-type=queue -value_size={} -threads={} -max_write_threads={} -time={} -path={} -num={} -space={} -collections={}".format(
        sz_value,
        n_thread_total,
        n_thread_write,
        t_duration,
        path_pmem, 
        n_operations,
        sz_pmem_file,
        n_collection)
    print("{0} {1} > {2}".format(exec, para_shared, path_report))

    # Benchmark hash
    # fill uniformly distributed kv
    new_para = para_shared + " -fill=1 -populate={}".format(populate_if_fill)
    report = path_report + "1.fill"
    print("Fill queue-type kv")
    os.system("{0} {1} > {2}".format(exec, new_para, report))

    # random read
    new_para = para_shared + " -fill=0 -read_ratio=1"
    report = path_report + "2.read_random"
    print("Random read queue-type kv")
    os.system("{0} {1} > {2}".format(exec, new_para, report))

    # read + update
    new_para = para_shared + " -fill=0 -read_ratio=0.5"
    report = path_report + "3.read_write_55"
    print("Mixed read/update hash-type kv")
    os.system("{0} {1} > {2}".format(exec, new_para, report))

    # push new kvs
    new_para = para_shared + " -fill=0 -read_ratio=0 -existing_keys_ratio=0"
    report = path_report + "4.insert"
    print("Insert new hash-type kv")
    os.system("{0} {1} > {2}".format(exec, new_para, report))

    os.system("rm -rf {0}".format(path_pmem))

if __name__ == "__main__":
    run_bench_mark()