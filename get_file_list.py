import requests, re, time

pattern_list = r'<img src="/icons/(?!back|blank).*?>.+\n'
pattern_list = re.compile(pattern_list)
pattern_href = r'(?<=href=").+(?=">)'
pattern_href = re.compile(pattern_href)

total_size = 0

def recursive_visit(url, out, ):
    global total_size
    r = requests.get(url).text
    list = pattern_list.findall(r)
    for line in list:
        isFolder, href, date, time, size = ana_line(line)
        fullLink = url + href
        #print('isFolder:', isFolder,',href:', href, 'date:', date, 'time:', time, 'size:', size)
        if(isFolder):
            recursive_visit(fullLink, out)
        else:
            out_put_line = fullLink + '\t' + date + ' ' + time + ' ' + size + '\n'
            total_size = total_size + convert_size(size)
            out.write(out_put_line)
            print(fullLink, 'total size =', total_size)


def ana_line(line):
    href = pattern_href.findall(line)[0]
    info = re.sub(r'.+</a>\s+|\s+$', '', line).split()
    if href[-1] == '/':
        isFolder = True
    else:
        isFolder = False
    return isFolder, href, info[0], info[1], info[2]


def get_file_list(url, output_file):
    global total_size
    with open(output_file, 'w') as out:
        recursive_visit(url, out)
        finish_info = 'Finish at ' + str(time.strftime("%b,%d %H:%M:%S", time.localtime()))  + ', Total size:' + str(total_size) + 'MB' + '\n'

        print(finish_info)
        out.write(finish_info)


def convert_size(size_str):
    if size_str[-1] == 'K':
        num = float(size_str[:-1])
        size_in_mb = num / 1024
    elif size_str[-1] == 'M':
        num = float(size_str[:-1])
        size_in_mb = num
    elif size_str [-1] == 'G':
        num = float(size_str[:-1])
        size_in_mb = num * 1024
    else:
        num = float(size_str)
        size_in_mb = num / 1024 / 1024
    return size_in_mb

if __name__ == "__main__":
    url = r'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2017_06/0010050103/'
    get_file_list(url, 'list.txt')
