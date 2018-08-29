#!/usr/bin/python


# Built-In Libraries
import json
import requests


class api:
    def __init__(self, api_key):
        self.api_key = api_key
        self.BASE_URL = "https://api.meraki.com/api/v0/"

    def get(self, uri):
        response = requests.get(
            url=self.BASE_URL+uri,
            headers={
                'X-Cisco-Meraki-API-Key': self.api_key,
                'Content-Type': 'application/json'
                })
        return response.json()

    def post(self, uri, data=None):
        if data:
            data = json.dumps(data, indent=4)
        response = requests.post(
            url=self.BASE_URL+uri,
            data=data,
            headers={
                'X-Cisco-Meraki-API-Key': self.api_key,
                'Content-Type': 'application/json'
                })
        try:
            return response.json()
        except Exception:
            return response

    def put(self, uri, data):
        data = json.dumps(data, indent=4)
        response = requests.put(
            url=self.BASE_URL+uri,
            data=data,
            headers={
                'X-Cisco-Meraki-API-Key': self.api_key,
                'Content-Type': 'application/json'
                })
        return response.json()
