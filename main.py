from bs4 import BeautifulSoup
import csv
from glob import glob

def parse(file: str):
  with open(f'{file.lower()}.html') as f:
    s = BeautifulSoup(f.read(), 'html.parser')
  res = []
  for tr in s.find_all('tr', class_='awsui-table-row'):
    blocks = list(map(lambda x: x.text.strip(), tr.select('td>span>span')))
    title = blocks[0]
    price = float(f"{(float(blocks[1].split()[0])*120*24*30.5):.1f}")
    vcpu = int(blocks[2])
    mem = float(blocks[3].split(' ')[0])
    res.append({'title': title, 'price': price, 'vcpu': vcpu, 'mem': mem})
  res = list(sorted(res, key=lambda x: x['price']))
  with open(f'{file}.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "vcpu", "mem"])
    writer.writeheader()
    writer.writerows(res)

for file in glob("*.html"):
  parse(file.split(".")[0])