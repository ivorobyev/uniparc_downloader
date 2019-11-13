import requests
import argparse
import urllib

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--taxon', help = 'organism identificator')
parser.add_argument('-f', '--format', help = 'output format')
args = parser.parse_args()

base_url = 'https://www.uniprot.org/uniparc/?query=organism:{0}&format={1}'


req = base_url.format(args.taxon, args.format)
print(req)
with urllib.request.urlopen(req) as f:
    response = f.read()

for a in response:
    print (a)
    print('---')