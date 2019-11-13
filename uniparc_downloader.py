import requests
import pandas as pd

taxon = 33926
format_ = 'fasta'
r = requests.get('https://www.uniprot.org/uniparc/?query=organism:'+str(taxon)+'&format='+format_)