from typing import List
import os
import requests


class Drehscheibe:
    DREHSCHEIBE_URL = os.getenv("DREHSCHEIBE_URL")
    DREHSCHEIBE_USER = os.getenv("DREHSCHEIBE_USER")
    DREHSCHEIBE_PW = os.getenv("DREHSCHEIBE_PW")

    def __init__(self) -> None:
        self.session = requests.Session()
        self.__login()
        self.__headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

    def __login(self) -> None:
        auth = {
            "username": self.DREHSCHEIBE_USER,
            "password": self.DREHSCHEIBE_PW,
        }
        response = self.session.post(
            f"{self.DREHSCHEIBE_URL}/apilogin", json=auth, timeout=10)
        response.raise_for_status()

    def get_data(self, uuid = "") -> List:
        model = "vehicles"
        if uuid:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}/{uuid}"
        else:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}"
        response = self.session.get(url, timeout=3, headers=self.__headers)
        response.raise_for_status()
        response_data = response.json()
        if isinstance(response_data, list):
            return response_data
        else:
            return [response_data]
