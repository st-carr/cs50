import re


test = "new york, ny 20202"
test1 = "new york, new york 20202"

#m = re.search('(?<=,)\w+', test)
g = re.match(r"(\w+\s?\w+?)\,\s*(\w+\s?\w+?)\s(\d+)", test1)
#print(m.group(0))
print(g.group(0))
print(g.group(1).title())
print(g.group(2).title())
print(g.group(3))
