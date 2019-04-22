from locust import HttpLocust, TaskSet, task
import numpy as np

max_users = 100

class UserBehavior(TaskSet): 
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        #self.login()
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        #self.logout()
        pass

    @task(1)
    def login(self):
        idx = np.random.randint(max_users)
        with self.client.post("/account/login", 
            json = {"username": "uname" + str(idx), "password": "pass" + str(idx)}, 
            catch_response=True) as response:
            if (response.status_code == 200):
                json_response_dict = response.json() 
                self.token_string = json_response_dict['token']
            elif response.status_code == 404:
                response.success()

    @task(1)
    def registration(self):
        idx = np.random.randint(max_users)
        with self.client.post("/account/registration",
        json = {"username": "uname" + str(idx), "password": "pass" + str(idx),
                "email": "mail" + str(idx) + "@mail.com", "screen_name": "sname" + str(idx),
                 "birth_date": "1999-01-01"}, catch_response = True) as response:
                 if response.status_code == 403:
                    response.success()

    @task(1)
    def forget_password(self):
        idx = np.random.randint(max_users)
        with self.client.post("/account/forget_password",
        json = {"email": "mail" + str(idx) + "@mail.com"}, catch_response = True) as response:
                if response.status_code == 403:
                    response.success()

    @task(1)
    def resend_email(self):
        idx = np.random.randint(max_users)
        with self.client.post("/account/registration/resend_email", 
        json = {"email": "mail" + str(idx) + "@mail.com"}, catch_response = True) as response:
                 if response.status_code == 403:
                    response.success()
    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000