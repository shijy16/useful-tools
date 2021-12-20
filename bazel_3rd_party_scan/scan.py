import os
import sys
import re

def get_files(dir_name):
    workspaces = []
    for root,dirs,files in os.walk(dir_name):
        for f in files:
            if f.lower().find('workspace') > -1:
                workspaces.append(os.path.join(root, f))
    return workspaces

def get_dep_in_ws(workspace):
    deps = []
    with open(workspace, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].find('http_archive(') > -1 \
                or lines[i].find('new_local_repository(') > -1 \
                    or lines[i].find('local_repository(') > -1:
                # print(lines[i])
                try:
                    idx = i
                    while(True):
                        idx += 1
                        if lines[idx].find('tf_http_archive(') > -1 \
                            or lines[idx].find('new_local_repository(') > -1 \
                                or lines[idx].find('local_repository(') > -1:
                            break
                        dep = re.search(r'name = \"([^\"]+)\"', lines[idx])
                        # print(dep)
                        if dep is None:
                            continue
                        deps.append(dep.group(1))
                        break
                except:
                    print('EROOR:', workspace)
    return deps

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scan.py TARGET_DIR')
        exit(0)
    target_dir = sys.argv[1]
    workspaces = get_files(target_dir)
    print(workspaces)
    deps = []
    for f in workspaces:
        deps += get_dep_in_ws(f)
    print(len(deps))
    print(set(deps))