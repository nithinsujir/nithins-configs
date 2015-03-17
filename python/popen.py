import subprocess

p1 = subprocess.Popen(['/bin/p4', 'change', '-o', '337845'], stdout = subprocess.PIPE)
output = p1.communicate()[0]

print output
output = output.replace('chongappa', 'abc')
p2 = subprocess.Popen(['/bin/p4', 'change', '-i'], stdin = subprocess.PIPE, stdout = subprocess.PIPE)

output = p2.communicate(input = output)[0]
print output
