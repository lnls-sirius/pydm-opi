#!/usr/bin/python3
from string import Template
t = Template("10.0.38.34:5${a} ")
print("export EPICS_CA_ADDR_LIST=\"\\")

aux = ''
for a in range(400, 900 , 2):
    if a % 20 == 0:
        print(aux + '\\')
        aux = ''
    aux += t.safe_substitute(a=a)
print("\"")
