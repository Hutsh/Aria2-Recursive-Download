import requests
from bs4 import BeautifulSoup
import os
import urllib.parse as urp
import sys, re

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
        path = re.sub(pattern, "./", url)
        path = re.sub("//", "/", path)
    else:
        file = os.path.basename(url)
        path = re.sub(file, '', url)
        path = localDir(path)
    return path

def recursiveDownload(urlList, arguments = ""):
    for url in urlList:
        if isPath(url):
            recursiveDownload(getNextLevel(url))
        else:
            local = localDir(url)
            cmd = 'aria2c -d ' + local + " " + arguments + " " + url
            cmd = re.sub("  ", " ", cmd)
            os.system(cmd)

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    # 	print("\n\nEnter URL to SCRAPE as COMMAND LINE ARGUMENT\n\n")
    # else:
	# 	recur(sys.argv[1], os.getcwd()+"/")
    url = r'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2017_06//0070010102/xti/'
    #next1 = getNextLevel('https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2017_06//0070010102/xti//event_cl/')
    recursiveDownload([url])
