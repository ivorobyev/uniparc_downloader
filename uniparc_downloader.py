import requests
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--taxon', help = 'organism identifier')
parser.add_argument('-f', '--format', help = 'output format')
args = parser.parse_args()

base_url = 'https://www.uniprot.org/uniparc/?query=organism:{0}&format={1}'

req = base_url.format(args.taxon, args.format)

print('collecting data for taxon-{0} in {1} format'.format(args.taxon, args.format))

s = requests.get(req)

#parse given data
m = str(s.text)
m = m.split('\n')
f_table = []
for a in m:
    f_table.append(a.split('\t'))

#write in file
file_name = 'uniparc_{0}_{1}_{2}'.format(args.taxon, args.format, time.time())
with open(file_name, 'w') as f:
    for a in f_table:
        f.write(str(a) + '\n')
    f.close()

print('elapsed_time: ' + str(time.time() - start_time))
print('data saved in file: ' + file_name)