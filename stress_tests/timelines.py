from locust import HttpLocust, TaskSet, task
import numpy as np

users = ["test_user2","test_user3"]
passwords = ["Pp111111","Pp111111"]
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
    def getkweekstimelineprofile(self):
        idx = np.random.randint(num_users)
        self.client.get("/kweeks/timelines/profile?username="+users[idx],headers={"TOKEN": self.token_string})

    @task(1)
    def getkweekstimelinehome(self):
        self.client.get("/kweeks/timelines/home",headers={"TOKEN": self.token_string})




class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000