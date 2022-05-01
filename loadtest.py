import time
from locust import HttpUser, task, between, events
import os, shutil
import numpy as np
import random
import string

class QuickstartUser(HttpUser):
	wait_time = between(1, 5)

	@events.test_start.add_listener
	def on_test_start(environment, **kwargs):
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
		numfiles = np.random.randint(1, 20)
		for i in range(numfiles):
			print("Generating file")
			size = np.random.randint(10, 1500)
			chars = ''.join([random.choice(string.ascii_letters) for i in range(size)]) #1
			filename = folder+'/testfile'+str(i)+'.txt'
			with open(filename, 'w') as f:
				f.write(chars)

	@task(3)
	def view_items(self):
		response = self.client.get("", name="getall")
		if len(response.json()) == 0 or not isinstance(response.json(), list):
			return
		choice = np.random.choice(response.json(), replace = False)
		response = self.client.get(f"/objs/{choice}", name="getfile")
		time.sleep(1)
			
	@task(3)
	def put_item(self):
		file = np.random.choice(os.listdir("testfiles"))
		f = open("testfiles/"+file)
		content = f.read()
		response = self.client.put('/objs/'+file, {'content': content}, name="putfile")

	@task
	def delete_item(self):
		response = self.client.get("")
		if len(response.json()) == 0 or not isinstance(response.json(), list):
			return
		choice = np.random.choice(response.json(), replace = False)
		r = self.client.delete("/objs/"+choice)

	def on_start(self):
	    	self.client.get("", name="getall")
        