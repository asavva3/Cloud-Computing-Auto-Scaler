import time
from locust import HttpUser, task, between
from locust.exception import RescheduleTask
import os, shutil
import numpy as np

class QuickstartUser(HttpUser):
	wait_time = between(1, 5)

	@task(3)
	def view_items(self):
		with self.client.get("", catch_response=True, name="getall") as response:
			if response.status_code == 429:
				raise RescheduleTask()
			if len(response.json()) == 0 or not isinstance(response.json(), list):
				return
			choice = np.random.choice(response.json(), replace = False)
			with self.client.get(f"/objs/{choice}", catch_response=True, name="getfile") as response:
				if response.status_code == 429:
					raise RescheduleTask()
				time.sleep(1)
	
	@task(3)
	def put_item(self):
		file = np.random.choice(os.listdir("testfiles"))
		f = open("testfiles/"+file)
		content = f.read()
		with self.client.put('/objs/'+file, {'content': content}, catch_response=True, name="putfile") as response:
			if response.status_code == 429:
					raise RescheduleTask()

	def on_start(self):
		with self.client.get("", catch_response=True, name="getall") as response:
			if response.status_code == 429:
				raise RescheduleTask()
		