import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--taxon', help = 'organism identificator')
parser.add_argument('-f', '--format', help = 'output format')
args = parser.parse_args()

base_url = 'https://www.uniprot.org/uniparc/?query=organism:{0}&format={1}'


req = base_url.format(args.taxon, args.format)

s = requests.get(req)
m = str(s.text)
m = m.split('\n')
f_table = []
for a in m:
    f_table.append(a.split('\t'))

print(f_table)