from django.core.management.base import BaseCommand
import csv, requests, json

class Command(BaseCommand):
    help = 'Import movies from csv file.'

    def __init__(self):
        self.token = ''

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="indicates csv file location")
        parser.add_argument('-u', '--username', type=str)
        parser.add_argument('-p', '--password', type=str)

    def login(self, username, password):
        data = {"username": username, "password": password}
        headers = {"content-type": "application/json"}
        r = requests.post('http://127.0.0.1:8000/api/v1/login/', data=json.dumps(data), headers=headers)
        response_json = r.json()
        print(response_json)
        self.token = response_json['token']

    def handle(self, *args, **kwargs):
        self.login(username=kwargs['username'], password=kwargs['password'])

        with open(kwargs['file']) as csvfile:
            movies = csv.DictReader(csvfile)
            for m in movies:
                temp = m['title'].split('(')
                title = temp[0].rstrip(' ')
                year = 0000 if len(temp) == 1 else temp[1].rstrip(')')
                genres = m['genres'].split('|')
                print("title: {}, year: {}, genres: {}".format(title, year, genres))
                headers = {"content-type":"application/json", "Authorization":"Token {}".format(self.token)}
                data = {'title':title, 'year':year}
                r = requests.post('http://127.0.0.1:8000/api/v1/movie/', data = json.dumps(data), headers=headers)
                print("response: {}.".format(r.status_code))
