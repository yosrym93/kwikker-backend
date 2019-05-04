from locust import HttpLocust, TaskSet, task
import numpy as np

users = ["test_user1", "test_user2", "ahly"]
passwords = ["pass", "pass", "ahlypassword"]
picture_path= "E:\youssef photos\PHOTOS\ATIZE5497.JPG"

num_users = 3

class UserBehavior(TaskSet): 
    profilebin = {'file': open(picture_path, 'rb')}

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

    @task(1)
    def notifications_unseen_count(self):
        self.client.get("/notifications/unseen_count",headers={"TOKEN": self.token_string})


    @task(1)
    def gettrends(self):
        self.client.get("/trends/",headers={"TOKEN": self.token_string})

    @task(1)
    def gettrendskweeks(self):
        self.client.get("/trends/kweeks?trend_id=1",headers={"TOKEN": self.token_string})

    @task(1)
    def search_users(self):
        idx = np.random.randint(num_users)
        self.client.get("/search/users?search_text="+users[idx],headers={"TOKEN": self.token_string})

    @task(1)
    def search_kweeks(self):
        idx = np.random.randint(num_users)
        self.client.get("/search/kweeks?search_text=barca",headers={"TOKEN": self.token_string})

    @task(1)
    def media(self):
        self.client.post("/media/",headers={"TOKEN": self.token_string},files=self.profilebin)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000