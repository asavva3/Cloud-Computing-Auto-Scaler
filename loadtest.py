import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
	wait_time = between(1, 5)

	@task
	def view_items(self):
		response = self.client.get("")
		lista = response.text	
		for item_id in response.json():
			print(item_id)
			response = self.client.get(f"/objs/{item_id}", name="/objs")
			print(response.text)
			time.sleep(1)

	def on_start(self):
	    	self.client.get("")
        
