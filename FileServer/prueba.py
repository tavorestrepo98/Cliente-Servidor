""" import hashlib

hasher = hashlib.md5()

hasher.update(b"Hola maricas")

print(hasher.hexdigest())


print(type(hasher.hexdigest())) """

import json

data = {}
data['Gustavo'] = {
    'name':[],
    'hashName':[]
}

data['Andrea'] = {
    'name':[],
    'hashName':[]
}
data['Gustavo']['name'].append("Hola")
data['Gustavo']['name'].append("Mamá")

print(data['Gustavo'])

""" data['Gustavo']['name'].append('pepino.jpg')
data['Gustavo']['hashName'].append('288a8e990cbf') """

with open('/home/gustavo/files/data.json', 'w') as f:
    json.dump(data, f, indent=4)

data2 = {}
with open('/home/gustavo/files/data.json', "r") as f:
    data2 = json.load(f)

""" a = [1, 2, 4]
print(type(data2))
print(data2.keys())
print(list(data2.keys()))
print(type(a)) """

nombre = 'Gustavo.jpg'
splt = nombre.split('.')
print(splt)