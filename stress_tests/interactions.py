from locust import HttpLocust, TaskSet, task
import numpy as np

users = ["dawood","test_user1"]
passwords = ["DaWood@123","pass"]
num_users = 2



class UserBehavior(TaskSet):
    token_string = ""

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        #self.logout()
        pass

    @task(1)
    def login(self):
        idx = np.random.randint(num_users)
        with self.client.post("/account/login", json = {"username": users[idx], "password": passwords[idx]}, catch_response=True) as response:
            if (response.status_code == 200):
                json_response_dict = response.json()
                self.token_string = json_response_dict['token']

    @task(1)
    def getfollowers(self):
        idx = np.random.randint(num_users)
        self.client.get("/interactions/followers?username="+users[idx],headers={"TOKEN": self.token_string})

    @task(1)
    def getfollowing(self):
        idx = np.random.randint(num_users)
        self.client.get("/interactions/following?username="+users[idx],headers={"TOKEN": self.token_string})

    @task(1)
    def post_block(self):
        self.client.post("/interactions/blocks",json = {"username":"test_user1"},headers={"TOKEN": self.token_string})
        self.client.delete("/interactions/blocks?username=test_user1", headers={"TOKEN": self.token_string})

    @task(1)
    def post_mute(self):
        self.client.post("/interactions/mutes",json = {"username":"test_user1"},headers={"TOKEN": self.token_string})
        self.client.delete("/interactions/mutes?username=test_user1", headers={"TOKEN": self.token_string})


    @task(1)
    def post_follow(self):
        self.client.post("/interactions/follow",json = {"username":"test_user1"},headers={"TOKEN": self.token_string})
        self.client.delete("/interactions/follow?username=test_user1", headers={"TOKEN": self.token_string})


    @task(1)
    def get_blocks(self):
        self.client.get("/interactions/blocks",headers={"TOKEN": self.token_string})

    @task(1)
    def get_mutes(self):
        self.client.get("/interactions/mutes",headers={"TOKEN": self.token_string})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000