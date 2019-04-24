from locust import Locust, TaskSet, task

def login(l):
    l.client.post("/api/v1/login/", {"username":"locust", "password":"locust"})

class MovieLoader(TaskSet):

    @task(1)
    def process_movie_csv(self):
        self.login()
        # read CSV file
        # generate movie

