import re

p = r'([^{=.,}]+)='

p = re.compile(p)

a = ['{aap8je=10}', '{aapje=10..}', '{aapje=..10}', '{aapje=10..10}', '{aapje=10,dan=10}', '{aapje=10,dan=10..12}', '{aapje=10,dan=10..}', '{aapje=10,dan=..10}', '{aapje=10,dan=10}', '{aapje=..10,dan=10..12}', '{aapje=10..12,dan=10..}', '{aapje=10..,dan=..10}']

b = set()
for i in a:
    for j in re.findall(p, i):
        b.add(j)

from pprint import pp
pp(b)