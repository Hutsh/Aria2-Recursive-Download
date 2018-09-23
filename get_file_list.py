import requests, re
from urllib.parse import urlparse

pattern_list = r'<img src="/icons/(?!back|blank).*?>.+\n'
pattern_list = re.compile(pattern_list)
pattern_href = r'(?<=href=").+(?=">)'
pattern_href = re.compile(pattern_href)

def recursive_visit(url, out):
    r = requests.get(url).text
    list = pattern_list.findall(r)
    for line in list:
        isFolder, href, date, time, size = ana_line(line)
        fullLink = url + href
        #print('isFolder:', isFolder,',href:', href, 'date:', date, 'time:', time, 'size:', size)
        if(isFolder):
            recursive_visit(fullLink, out)
        else:
            out_put_line = fullLink + '\n'
            out.write(out_put_line)
            print(fullLink, size)


def ana_line(line):
    href = pattern_href.findall(line)[0]
    info = re.sub(r'.+</a>\s+|\s+$', '', line).split()
    if href[-1] == '/':
        isFolder = True
    else:
        isFolder = False
    return isFolder, href, info[0], info[1], info[2]


def get_file_list(url, output_file):
    with open(output_file, 'w') as out:
        recursive_visit(url, out)


if __name__ == "__main__":
    url = r'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2017_06/0010050103/'
    get_file_list(url, 'list.txt')