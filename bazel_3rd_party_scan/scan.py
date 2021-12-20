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

def get_py_files(dir_name):
    py_files = []
    for root,dirs,files in os.walk(dir_name):
        for f in files:
            if f.endswith('.py'):
                py_files.append(os.path.join(root, f))
    return py_files

def get_imports_in_py(py_file):
    imports = []
    try:
        with open(py_file, 'r') as f:
            for line in f.readlines():
                if line.find('import ') > -1:
                    res = re.search(r'^from ([a-zA-Z0-9_]+) import', line)
                    if res is None:
                        res = re.search(r'^import ([a-zA-Z0-9_]+)', line)
                    try:
                        res = res.group(1)
                        if res.find('.') > -1:
                            res = res.split('.')[0]
                    except:
                        None
                    if res.find('torch') == -1 and res.find('tensorflow') == -1:
                        imports.append(res)
    except:
        None
        # print('ERROR:', py_file)
    # print(imports)
    imports = list(set(imports))
    return imports

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
    # print(len(deps))
    # print(set(deps))

    py_deps = []
    py_files = get_py_files(target_dir)
    for f in py_files:
        py_deps += get_imports_in_py(f)
    py_deps = py_deps
    # print(py_deps)
    res = deps + py_deps
    res = set(res)
    print(len(res))
    print(res)