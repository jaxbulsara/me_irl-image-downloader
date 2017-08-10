import os

os.rename('nicknames.txt', 'temp_nicknames.txt')

f = open('nicknames.txt', 'w')
f_tmp = open('temp_nicknames.txt', 'r')
f_new = open('removed_nicknames.txt', 'w')

i = 0
j = 0
k = 0

for line in f_tmp.readlines():
	i += 1
	if 'John' in line:
		j += 1
		f_new.write(line)
	else:
		k += 1
		f.write(line)

f.close()
f_tmp.close()
f_new.close()

# make sure all lines are accounted for before deleting temporary file
if i == j + k:
	os.remove('temp_nicknames.txt')
else:
	print('Error: some lines were lost.')