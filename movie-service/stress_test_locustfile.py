"""
locust -f stress_test_locustfile.py
"""

from locust import HttpLocust, TaskSet, task

def login(l):
    l.client.post("/")
