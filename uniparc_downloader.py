import requests
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--taxon', help = 'organism identifier')
parser.add_argument('-f', '--format', help = 'output format')
args = parser.parse_args()

formats = ['tab', 'fasta']
if args.format not in formats:
    raise NameError('\033[91m' + 'ERROR: unknown data format' + '\033[91m') 

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
    print('\033[91m' + 'CONNECTION ERROR: server unavailable' + '\033[91m') 
    exit()

print('Collecting data for taxon-{0} in {1} format'.format(args.taxon, args.format))

#define output filename
filename = 'uniparc_{0}_{1}_{2}.csv'.format(args.taxon, args.format, time.time())

def download_file(url, filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
        print('Download complete')
    except:
        print('\033[91m' + 'CONNECTION ERROR: server unavailable' + '\033[91m')
        exit()

download_file(req, filename)
    
print('\033[92m' + 'elapsed_time: ' + str(time.time() - start_time) + '\033[92m')
print('\033[92m' + 'data saved in file: ' + filename + '\033[92m')