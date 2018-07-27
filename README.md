# Aria2 Recursive Download
#### Usage: 

```ddld.py [-i|--input-file,[path]][-x|--max-connection,[number|'m']] [-p|--proxy,[http://][USER:PASSWORD@]HOST[:PORT]][-h|--help] [-d | --dir, [directory]]```

#### Description

- -i,--input-file         Downloads the URIs listed in FILE
- -x,--max-connection     The maximum number of connections to one server for each download. Default: 1, MAX: 16
- -p,--proxy              Set proxy server(http)
- -d,--dir                Save directories to
- -h,--help               Display help information.



#### Example

   ```python ddld.py -x 8 -i test.txt -d ./ -p 127.0.0.1:1080```





---



A simple scraper and bash script combination to download open directories recursively using aria2 instead of wget.

I use python BeautifulSoup to scrape an open directory and make a directory structure with relevant link to files stored in links.txt
Then the simple bash script just goes into every directory and downloads the files in the links.txt using aria2c

The scraper will need some tweaking based on what directory you are trying to download.
So consider this as just a bare body scraper that needs to be customized according the situation and requirement.
