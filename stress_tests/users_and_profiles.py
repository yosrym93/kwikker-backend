from locust import HttpLocust, TaskSet, task
import numpy as np



users = ["dawood","ahly"]
passwords = ["DaWood@123","123456"]
num_users = 2
profile_picture_path= "E:\youssef photos\PHOTOS\ATIZE5497.JPG"
banner_path="E:\youssef photos\PHOTOS\ATIZE5497.JPG"

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
    def get_profile(self):
        idx = np.random.randint(num_users)
        self.client.get("/user/profile",headers={"TOKEN": self.token_string},params={"username":users[idx]})


    @task(1)
    def update_bio_screenname(self):
        idx = np.random.randint(num_users)
        self.client.patch("/user/profile",json = {"bio": "bio" , "screen_name": users[idx]+"updated"},headers={"TOKEN": self.token_string})

    @task(1)
    def banner(self):
        self.client.post("/user/profile_banner",headers={"TOKEN": self.token_string},files=self.bannerbin)
        self.client.delete("/user/profile_banner", headers={"TOKEN": self.token_string})

    @task(1)
    def profile_picture(self):
        self.client.post("/user/profile_picture",headers={"TOKEN": self.token_string},files=self.profilebin)
        self.client.delete("/user/profile_picture", headers={"TOKEN": self.token_string})


    @task(1)
    def update_email(self):
        self.client.put("/user/email",headers={"TOKEN": self.token_string}, json = {"email": self.email})
        if(self.email == "newEmail@gmail.com"):
            self.email= "newEmail@yahoo.com"
        else:
            self.email = "newEmail@gmail.com"

    @task(1)
    def get_email(self):
        self.client.get("/user/email",headers={"TOKEN": self.token_string})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000