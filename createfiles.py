import os
import numpy as np
import string
import random

folder = 'testfiles'
for filename in os.listdir(folder):
	file_path = os.path.join(folder, filename)
	try:
		if os.path.isfile(file_path) or os.path.islink(file_path):
			os.unlink(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)
	except Exception as e:
		print('Failed to delete %s. Reason: %s' % (file_path, e))
numfiles = 30
for i in range(numfiles):
	print("Generating file")
	size = np.random.randint(1000000, 5000000)
	chars = ''.join([random.choice(string.ascii_letters) for i in range(size)]) #1
	filename = folder+'/testfile'+str(i)+'.txt'
	with open(filename, 'w') as f:
		f.write(chars)