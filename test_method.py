from unittest import TestCase

import requests



class TestUserRequest(TestCase):
    url = 'http://192.168.1.183:7000/user'
    def test_login(self):
        resp = requests.get(self.url,
                            json={
                                'name': 'zhoujielun',
                                'pwd': '123'
                            })
        print(resp.json())

