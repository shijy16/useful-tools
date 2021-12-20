import requests
from bs4 import BeautifulSoup
import json
import re
import csv

target_set = ['mkl', 'mkl_headers', 'com_github_glog', 'cuda', 'rules_python', 'bazel_skylib', 'cudnn', 'eigen', 'sleef', 'tensorpipe', 'onnx', 'pybind11', 'rules_cuda', 'content', 'com_google_protobuf', 'com_github_gflags_gflags', 'fmt', 'gloo', 'cpuinfo', 'ideep', 'asmjit', 'tbb', 'foxi', 'com_google_googletest', 'fbgemm', 'mkl_dnn', 'pybind11_bazel']
output_file = 'output.csv'


cve_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
headers = {'User-Agent': user_agent}

res = []


for t in target_set:
    t = t.replace('_archive', '').replace('com_', '').replace('github_', '').replace('google_', '')
    r = None
    try:
        r = requests.get(cve_url + t, headers=headers, timeout=1)
    except:
        res.append([t, 'TIMEOUT'])
        continue
    if r.status_code != 200:
        print('CONNECTION ERROR!')
        res.append([t, 'TIMEOUT'])
    else:
        try:
            content = r.text
            count = re.search('There are <b>([0-9]+)</b> CVE Records that match your search.', content).group(1)
            print(t, count)
            res.append([t, count])
        except:
            print('MATCH ERROR:', t)
            res.append([t, 'MATCH_ERROR'])

    with open(output_file, 'w', newline ='') as f:  
        writer = csv.writer(f)
        writer.writerow(['dep', 'cves'])
        for t in res:
            writer.writerow(t)
