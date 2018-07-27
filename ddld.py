import requests
from bs4 import BeautifulSoup
import os
import urllib.parse as urp
import sys, re, getopt

opt = {'connections': '1', }

def assure_path_exists(path):
    if not os.path.exists(path):
            os.makedirs(path)

def get_domain(link):
    return '{uri.scheme}://{uri.netloc}'.format(uri=urp.urlparse(link))

def getNextLevel(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    icons = soup.find_all("img")

    dirList = []
    for itag in icons:
        if '/icons/' in itag['src'] and ('blank.gif' not in itag['src']) and ('back.gif' not in itag['src']):
            next = itag.findNext()
            dirList.append(url + "/" + next['href'])

    return dirList

def isPath(url):
    return url.endswith('/')

def localDir(url):
    if isPath(url):
        pattern = r"https?://[\w\._]+/{1,2}[\w\._]+/{1,2}[\w\._]+/{1,2}[\w\._]+/{1,2}[\w\._]+/{1,2}[\w\._]+/{1,2}"
        path = re.sub(pattern, "/", url)
        path = re.sub("//", "/", path)
    else:
        file = os.path.basename(url)
        path = re.sub(file, '', url)
        path = localDir(path)
    return path

def recursiveDownload(aria2cPath, urlList, arguments):
    for url in urlList:
        print(url)
        if isPath(url):
            recursiveDownload(aria2cPath, getNextLevel(url), arguments)
        else:

            apath = os.path.abspath(opt['savepath'] + localDir(url))
            print(apath)
            arguments += " -d " + apath

            cmd = aria2cPath + " " + arguments + " " + url
            print(cmd)
            cmd = re.sub("  ", " ", cmd)
            os.system(cmd)


def usage():
    """
The output  configuration file contents.
Usage: ddld.py [-i|--input-file,[path]] [-x|--max-connection,[number|'m']] [-p|--proxy,[http://][USER:PASSWORD@]HOST[:PORT]] [-h|--help] [-d | --dir, [directory]]
Description
            -i,--input-file         Downloads the URIs listed in FILE
            -x,--max-connection     The maximum number of connections to one server for each download. Default: 1, MAX: 16
            -p,--proxy              Set proxy server(http)
            -d,--dir                Save directories to
            -h,--help               Display help information.
for example:
    python ddld.py -i downloadList.txt
    python ddld.py -x 8
    python ddld.py -p 127.0.0.1:8119
    python ddld.py -d ./download
"""

def isValidProxy(addr):
    ipPattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))"
    try:
        ip, port = addr.split(":")
    except Exception as e:
        print("Wrong Proxy format")
        return False
    if not re.match(ipPattern, ip):
        print("Wrong Proxy format")
        return False
    if int(port) < 1 or int(port) > 65535:
        print("Wrong Proxy format")
        return False
    return True

def checkProxy(proxy):
    try:
        requests.get(
            "http://example.com",
            proxies={'http': proxy},
            timeout=0.5
        )
    except Exception as e:
        print("Failed connected to proxy server")
        sys.exit(1)
    else:
        return True

def getOpt():
    try:
        options, args = getopt.getopt(sys.argv[1:], "i:x:p:d:h", ["--input-file=", "--max-connection=", "--proxy=", "--dir=" "help"])
    except getopt.GetoptError as err:
        print(str(err))
        print(usage.__doc__)
        sys.exit(1)

    ariaArg = ""
    # print("options>>", o, "<< argu>>", a, "<<")


    for o, a in options:
        if o in ("-i", "--input-file"):
            try:
                with open(a,'r'):
                    pass
                opt['input'] = os.path.abspath(a);
            except Exception as e:
                print(e)
                sys.exit(1)
        elif o in ("-x", "--max-connection"):
            if int(a) > 0 and int(a) <= 16:
                opt['connections'] = a;
            else:
                print('argument "-x" must in range 1-16')
                sys.exit(1)
        elif o in ("-p", "--proxy"):
            if isValidProxy(a):
                checkProxy(a)
                opt['proxy'] = a
            else:
                sys.exit(1)
        elif o in ("-d", "--dir"):
            p = os.path.abspath(a)
            if os.path.exists(p):
                opt['savepath'] = p
            else:
                print("Save directory not exsits")
                sys.exit(1)
    return opt

if __name__ == "__main__":

    opt = getOpt()
    if not 'input' in opt:
        print("No input file in arguments")
        sys.exit(1)
    if not 'savepath' in opt:
        print("No save directory in arguments")
        sys.exit(1)
    print(opt)

    urlList = []
    with open(opt['input'], 'r') as f:
        for line in f:
            urlList.append(line.strip('\n'))

    downloadArg = '-x ' + opt['connections'] + " -k 1048576"
    if 'proxy' in opt:
        downloadArg += " --all-proxy=" + opt['proxy']
    print(downloadArg)

    aria2cPath = re.sub(os.path.basename(sys.argv[0]), "", sys.argv[0]) + "aria2\\aria2c.exe"
    aria2cPath = os.path.abspath(aria2cPath)


    recursiveDownload(aria2cPath, urlList, downloadArg)
