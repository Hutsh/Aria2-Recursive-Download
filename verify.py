from urllib.parse import urlparse
import re, os, sys

def get_local_downloaded_file(url):
    o = urlparse(url)
    out = os.path.basename(o.path)
    dir = re.sub(out, '', o.path)
    return dir + out

def verify(listfile):
    outf = open('verify_' + listfile, 'w')

    with open(listfile, 'r') as lf:
        for line in lf:
            if line[:4] == 'http':
                url = re.sub(r'\t.+', '', line.strip('\n'))
                ldf = get_local_downloaded_file(url)
                if os.path.exists(ldf) :
                    outf.write(url + '\tOK!\n')
                else:
                    outf.write(url + '\tMISSING!\n')
            else:
                pass
    outf.close()


if __name__ == "__main__":
    #argument: url list only
    ##########################################

    fileinfo = str(sys.argv[1])

    verify(fileinfo)
