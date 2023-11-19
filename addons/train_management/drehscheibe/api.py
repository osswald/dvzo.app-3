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
        self.__timeout = 5

    def __login(self) -> None:
        auth = {
            "username": self.DREHSCHEIBE_USER,
            "password": self.DREHSCHEIBE_PW,
        }
        response = self.session.post(
            f"{self.DREHSCHEIBE_URL}/apilogin", json=auth, timeout=10)
        response.raise_for_status()

    def __get_data(self, model, uuid = "") -> List:
        if uuid:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}/{uuid}"
        else:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        response = self.session.get(url, timeout=self.__timeout, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if isinstance(response_data, list):
            return response_data
        else:
            return [response_data]

    def __post_data(self, model, body, headers, files=None, uuid = ""):
        if uuid:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}/{uuid}"
        else:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}"

        if files:
            response = self.session.post(
                url, data=body, files=files, timeout=self.__timeout, headers=headers)
        else:
            response = self.session.post(
                url, data=body, timeout=self.__timeout, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if isinstance(response_data, list):
            return response_data
        else:
            return [response_data]

    def get_vehicles(self, uuid = "") -> List:
        model = "vehicles"
        return self.__get_data(model, uuid)

    def get_vehicle_defects(self, uuid) -> List:
        model = "open-tasks"
        return [uuid, self.__get_data(model, uuid)]

    def post_vehicle_defects(self, uuid) -> List:
        model = "repair-task"
        files = None
        headers = {
            "accept": "application/json",
            "content-type": "multipart/form-data",
        }
        body = {
            "defectTitle": "Test",
            "defectDescription": "Test",
            "date": "01.11.2021",
            "time": "13:00",
            "trainNumber": "431K",
            "whereAtVehicle": "roof",
            "isAccident": "no",
            "isSecurityRelated": False,
        }
        return self.__post_data(model, body, headers, files, uuid)

    def post_day_planning(self):
        model = "completed-trip"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        body = {
            "name": "Test",
            "date": "01.11.2021",
            "timeStart": "13:00",
            "completedDate": "01.13.2021",
            "completedNote": "Test",
            "matrix": [
                {
                    "vehicle": "b96bf00d-94c4-40c3-b364-affcb6d53549",
                    "km": "15.39",
                    "railline": [
                        {
                            "stationStart": "Test",
                            "stationEnd": "Test",
                        },
                        {
                            "stationStart": "Gugus",
                            "stationEnd": "Dadaa",
                        },
                    ],
                },
            ],
        }
        return self.__post_data(model, body, headers)
