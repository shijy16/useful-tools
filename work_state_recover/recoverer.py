import sys
import os
import subprocess
import time
import psutil
import json

def get_opened_files(p, postfixs):
    f = p.open_files()
    files = []
    for postfix in postfixs:
        files += [ x.path for x in f if x.path.endswith(postfix) > 0]
    return files



targets = {}
targets['word'] = {}
targets['word']['pname'] = 'WINWORD.EXE'
targets['word']['postfixs'] = ['.doc', '.docx']
targets['pdf'] = {}
targets['pdf']['pname'] = 'Acrobat.exe'
targets['pdf']['postfixs'] = ['.pdf']
# targets['md'] = {}
# targets['md']['PNAME'] = 'Typora.exe'
# targets['md']['postfixs'] = ['.md']

def save_work_state(fname='work_state.json'):
    opened_files = {}
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        for k in targets.keys():
            if targets[k]['pname'] == p.name():
                print(p.name())
                targets[k]['exec'] = p.cmdline()[0]
                targets[k]['files'] = get_opened_files(p, targets[k]['postfixs'])
    json_str = json.dumps(targets, indent=4, ensure_ascii=False)
    with open(fname, 'w', encoding='utf8') as json_file:
        json_file.write(json_str)

def load_work_state(fname='work_state.json'):
    json_str = None
    with open(fname, 'r', encoding='utf8') as json_file:
        json_str = json_file.read()
    targets = json.loads(json_str)
    for k in targets.keys():
        prefix = targets[k]['exec']
        for f in targets[k]['files']:
            print(prefix, f)
            subprocess.Popen([prefix, f],  creationflags = subprocess.CREATE_NEW_CONSOLE)
            time.sleep(3)

def usage():
    print('usage: python recoverer.py load/save (file_name)\nfile_name is default set as work_state.json')
    exit(0)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == 'save':
        save_work_state()
    elif sys.argv[1] == 'load':
        load_work_state()
    else:
        usage()

