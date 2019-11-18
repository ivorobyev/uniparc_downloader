import requests
import argparse
import time
import os
import sys

#terminal color codes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

#function to download file by chunks
def download_file(url, filename, rownumber):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                complete = 0
                for chunk in r.iter_content(chunk_size=10000000): 
                    if chunk:
                        f.write(chunk)
                        complete += len(str(chunk).split('\\n'))
                        progress(complete, rownumber, status='Downloading')
        print('Download complete')

if __name__ == '__main__' :
    print(bcolors.OKBLUE + 'Uniparc downloader runing' + bcolors.ENDC)
    print(bcolors.OKBLUE + '-------------------------' + bcolors.ENDC)

    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--taxon', help = 'organism identifier')
    parser.add_argument('-f', '--format', help = 'output format')
    args = parser.parse_args()

    formats = ['tab', 'fasta']
    if args.format not in formats:
        raise NameError(bcolors.FAIL + 'ERROR: unknown data format' + bcolors.ENDC) 

    #make url for request
    base_url = 'https://www.uniprot.org/uniparc/?query=organism:{0}&format={1}&columns:sequence'
    req = base_url.format(args.taxon, args.format)

    #print version
    try:
        r = requests.head(req)
        print('UniProt Release: ' + r.headers['X-UniProt-Release'])
        print('Last Modified: ' + r.headers['Last-Modified'])
        print('Total rows: ' + r.headers['X-Total-Results'])
    except:
        print(bcolors.FAIL + 'CONNECTION ERROR: server unavailable' + bcolors.ENDC) 
        exit()

    if int(r.headers['X-Total-Results']) == 0:
        print(bcolors.OKGREEN + 'Dataset has no records, nothing to download' + bcolors.ENDC)
        exit()

    print('Collecting data for taxon-{0} in {1} format'.format(args.taxon, args.format))

    #define output filename
    filename = 'uniparc_{0}_{1}_{2}.csv'.format(args.taxon, 
                                                args.format, 
                                                time.strftime("%Y-%m-%d-%H-%M", time.localtime()))

    #downloading file
    download_file(req, filename, int(r.headers['X-Total-Results']))
        
    print(bcolors.OKGREEN  + 'elapsed_time: ' + str(time.time() - start_time) + bcolors.ENDC)
    print(bcolors.OKGREEN + 'data saved in file: ' + filename + bcolors.ENDC)