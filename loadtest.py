import time
from locust import HttpUser, task, between, events
import os, shutil
import numpy as np
import random
import string

class QuickstartUser(HttpUser):
	wait_time = between(1, 5)

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

	def on_start(self):
	    	self.client.get("", name="getall")
        