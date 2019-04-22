from locust import HttpLocust, TaskSet, task
import numpy as np
users = ["test_user2", "test_user3"]
passwords = ["Pp111111","Pp111111"]
num_users = 2
banner_path= "E:\youssef photos\PHOTOS\AAFR9688.JPG"
profile_picture_path= "E:\youssef photos\PHOTOS\ATIZE5497.JPG"

class UserBehavior(TaskSet):
    bannerbin = {'file': open(banner_path, 'rb')}
    profilebin = {'file': open(profile_picture_path, 'rb')}

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
    def getprofile(self):
        idx = np.random.randint(num_users)
        self.client.get("/user/profile",headers={"TOKEN": self.token_string},params={"username":users[idx]})


    @task(1)
    def updatebioscreenname(self):
        idx = np.random.randint(num_users)
        self.client.patch("/user/profile",json = {"bio": "bio" , "screen_name": users[idx]+"updated"},headers={"TOKEN": self.token_string})

    @task(1)
    def banner(self):
        self.client.put("/user/profile_banner",headers={"TOKEN": self.token_string},files=self.bannerbin)
        self.client.delete("/user/profile_banner", headers={"TOKEN": self.token_string})

    @task(1)
    def profilepicture(self):
        self.client.put("/user/profile_picture",headers={"TOKEN": self.token_string},files=self.profilebin)
        self.client.delete("/user/profile_picture", headers={"TOKEN": self.token_string})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000