from locust import HttpLocust, TaskSet, task
import numpy as np

users = ["test_user1", "test_user2", "ahly"]
passwords = ["pass", "pass", "ahlypassword"]

num_users = 3

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
        with self.client.post("/account/login", 
            json = {"username": users[idx], "password": passwords[idx]}, catch_response=True) as response:
            if (response.status_code == 200):
                json_response_dict = response.json() 
                self.token_string = json_response_dict['token']
            else:
                response.failure("Cannot Login With User" + str(idx))


    @task(1)
    def notifications(self):
        self.client.get("/notifications/",headers={"TOKEN": self.token_string})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000