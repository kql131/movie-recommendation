from locust import Locust, TaskSet, task
import csv

def login(l):
    l.client.post("/api/v1/login/", {"username":"locust", "password":"locust"})

class MovieLoader(TaskSet):

    def load_movies_from_csv():
        with open('movies.csv') as csvfile:
            return csv.DictReader()

    movies_dict = load_movies_from_csv()

    @task(1)
    def process_movie_csv(self):
        
    

