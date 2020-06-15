import re
pattern = re.compile(r"scores={(?:(\w+)=[.\d]*)(?:,(\w+)=[.\d]*)?(?:,(\w+)=[.\d]*)?(?:,(\w+)=[.\d]*)?(?:,(\w+)=[.\d]*)?")
result = re.findall(pattern,"@e[distance=..10,scores={score_1=19,score_2=14}]]\n@e[scores={score_1=19,score_2=14}]]")
print(result)


pattern = re.compile(r"(?:scores={|\d|,)\s*([^|{}]+?)(?=\s*?(?:,|}))")
result = re.findall(pattern,"@e[scores={aap=3,   baok=3,  baad=3},tag=boy]")
print(result)