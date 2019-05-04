from locust import HttpLocust, TaskSet, task
import numpy as np


users = ["dawood","ahly"]
passwords = ["DaWood@123","123456"]
num_users = 2

class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        #self.logout()
        pass

    def login(self):
        idx = np.random.randint(num_users)
        with self.client.post("/account/login", json = {"username": users[idx], "password": passwords[idx]}, catch_response=True) as response:
            if (response.status_code == 200):
                json_response_dict = response.json()
                self.token_string = json_response_dict['token']

    @task(1)
    def get_dm(self):
        self.client.get("/direct_message/?username=test_user2",headers={"TOKEN": self.token_string})


    @task(1)
    def get_dm_conversations(self):
        self.client.get("/direct_message/conversations",headers={"TOKEN": self.token_string})

    @task(1)
    def get_dm_recent_conversationers(self):
        self.client.get("/direct_message/recent_conversationers",headers={"TOKEN": self.token_string})

    @task(1)
    def post_recent_conversationers(self):
        idx = np.random.randint(num_users)
        self.client.post("/direct_message/recent_conversationers",json = {"search_user" : users[idx]},headers = {"TOKEN": self.token_string})

    @task(1)
    def post_dm(self):
        idx = np.random.randint(num_users)
        self.client.post("/direct_message/",json = {"text": "new message","username": users[idx],"media_id": "nullable string"},headers = {"TOKEN": self.token_string})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000