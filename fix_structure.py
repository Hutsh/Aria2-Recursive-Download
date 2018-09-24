from urllib.parse import urlparse
import re, os
import shutil

def generate_cmd(url, proxy=''):
    dir, out = get_local_path(url)
    cmd = url + '\n  dir=.' + dir + '\n  out=' + out
    if proxy == '':
        return cmd
    else:
        cmd = cmd + '\n  http-proxy=' + proxy
        return cmd

def get_local_path(url):
    o = urlparse(url)
    out = os.path.basename(o.path)
    dir = re.sub(out, '', o.path)
    return dir, out


def start(listfile):
    with open(listfile, 'r') as f:
        for line in f:
            url = line.strip('\n')
            dir, file = get_local_path(url)
            des = '.' + dir + file
            despath = '.'+dir
            try:
                shutil.move(file, des)
            except IOError as e:
                pass
if __name__ == "__main__":
    file = r'2017_06.txt'
    start(file)