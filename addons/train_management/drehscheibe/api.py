from typing import List
import os
import requests
import logging
from base64 import b64decode


log = logging.getLogger(__name__)


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

    def __post_data(self, model, body, headers, upload=None, uuid="", form_data=False):
        if uuid:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}/{uuid}"
        else:
            url = f"{self.DREHSCHEIBE_URL}/api/{model}"

        if form_data:
            files = {key: (None, value) for key, value in body.items()}

            for key, (name, data) in upload.items():
                if data:
                    files[key] = (name, b64decode(data))
        else:
            files = upload
       
        response = self.session.post(
            url, json=body, files=files, timeout=self.__timeout, headers=headers)
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

    def post_vehicle_defects(self, defect) -> List:
        model = "repair-task"
        headers = {
            "accept": "application/json",
        }
        upload = {
                "filePath01": ("image1", defect.image1),
                "filePath02": ("image2", defect.image2),
                "filePath03": ("image3", defect.image3),
                }
        body = {
            "defectTitle": defect.defectTitle,
            "defectDescription": defect.defectDescription,
            "date": defect.date.strftime("%d.%m.%Y"),
            "time": "12:00",
            "trainNumber": defect.trainNumber,
            "whereAtVehicle": defect.whereAtVehicle,
            "isAccident": defect.isAccident,
            "isSecurityRelated": defect.isSecurityRelated,
        }
        return self.__post_data(model, body, headers, upload, defect.vehicle.ds_id, form_data=True)

    def post_day_planning(self):
        model = "completed-trip"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        body = {
            "name": "Dampf Zug",
            "date": "12.09.2023",
            "timeStart": "09:00",
            "timeEnd": "18:00",
            "responsiblePerson": "Hans Muster",
            "location": "Sihlwald",
            "completedDate": "12.10.2023",
            "completedNote": "Notiz...",
            "matrix": [
                {
                    "vehicle": "b96bf00d-94c4-40c3-b364-affcb6d53549",
                    "km": "33",
                    "railline": [
                        {
                            "stationStart": "BMA",
                            "stationEnd": "HI"
                        },
                        {
                            "stationStart": "BMA",
                            "stationEnd": "BAEW"
                        }
                    ]
                }
            ]
        }

        return self.__post_data(model, body, headers)


if __name__ == "__main__":
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
    drehscheibe = Drehscheibe()
    drehscheibe.post_day_planning()
