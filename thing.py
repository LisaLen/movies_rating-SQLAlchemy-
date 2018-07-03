f = open('seed_data/u.item')

max_t = 0
max_u = 0

for l in f:
    line = l.split('|')
    if len(line[1]) > max_t:
        max_t = len(line[1])
    if len(line[4]) > max_u:
        max_u = len(line[4])

print(max_t)
print(max_u)