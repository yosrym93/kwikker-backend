from locust import HttpLocust, TaskSet, task
import numpy as np

users = ["dawood","ahly"]
passwords = ["DaWood@123","123456"]
num_users = 2
hashtags = ["hashtag1", "hashtag2","hashtag3"]

kweek_number = "3"

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
                response.failure("Cannot Login With User: " + str(idx))


    @task(1)
    def get_kweeks(self):
        self.client.get("/kweeks/?id=" + kweek_number,
        headers={"TOKEN" : self.token_string})


    @task(1)
    def create_kweek(self):
        idx = np.random.randint(num_users)
        mode = np.random.randint(3)
        if (mode == 1):
            self.client.post("/kweeks/",
            json = {"text": "WOW" + "@" + users[idx] + " how are you?", "reply_to": None,"media_id": "nullable string"},
            headers={"TOKEN" : self.token_string})
        elif (mode == 2):
            self.client.post("/kweeks/",
            json = {"text": "WOW" + "#" + hashtags[idx] + "_end WE ROCK", "reply_to": None,"media_id": "nullable string"},
            headers={"TOKEN" : self.token_string})
        else:
            self.client.post("/kweeks/",
            json = {"text": "Hi Kweek", "reply_to": None,"media_id": "nullable string"},
            headers={"TOKEN" : self.token_string})


    @task(1)
    def create_reply(self):
        idx = np.random.randint(num_users)
        mode = np.random.randint(3)
        if (mode == 1):
            self.client.post("/kweeks/",
            json = {"text": "WOW" + "@" + users[idx] + " how are you?", "reply_to": kweek_number,"media_id": "nullable string"},
            headers={"TOKEN" : self.token_string})
        elif (mode == 2):
            self.client.post("/kweeks/",
            json = {"text": "WOW" + "#" + hashtags[idx] + "_end WE ROCK", "reply_to": kweek_number,"media_id": "nullable string"},
            headers={"TOKEN" : self.token_string})
        else:
            self.client.post("/kweeks/",
            json = {"text": "Hi Reply", "reply_to": kweek_number,"media_id": "nullable string"},
            headers={"TOKEN" : self.token_string})


    @task(1)
    def like_kweek(self):
        self.client.post("/kweeks/like",
        json = {"id": kweek_number},
        headers={"TOKEN" : self.token_string})

    @task(1)
    def get_kweeks_likers(self):
        self.client.get("/kweeks/likers?id=" + kweek_number,
        headers={"TOKEN" : self.token_string})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000