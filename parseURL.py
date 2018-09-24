from urllib.parse import urlparse
import re, os

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


def generate_cmd_file(listfile,outfile, proxylist):
    proxy = []
    for i in range(len(proxylist)):
        proxy.append('\n  http-proxy=' + proxylist[i])
    proxy.append('')

    nproxy = len(proxy)
    i = nproxy - 1;

    outf = open(outfile, 'w')
    with open(listfile, 'r') as lf:
        for line in lf:
            url = re.sub(r'\t.+\n', '', line)
            cmd = generate_cmd(url) + proxy[i] + '\n'
            i += 1
            if(i == nproxy):
                i = 0
            print(cmd, end='')
            outf.write(cmd)
    outf.close()

if __name__ == "__main__":
    #fileinfo is the file contains download files information.
    #fileinfo example:
    #https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2017_06/0010050103/auxil/ni0010050103.att.gz	06-Mar-2018 16:55 1.0M

    #example aria2 download command:
    #aria2c --input-file=cmdout.txt --log=aria.log --max-concurrent-downloads=15 --continue=true --min-split-size=20M
    ####################arguments#############
    proxylist = ['http://45.33.109.91:7333','http://23.239.27.216:7333']
    fileinfo = 'a.txt'
    cmdout = 'cmdout.txt'
    ##########################################
    generate_cmd_file(fileinfo, cmdout ,proxylist)