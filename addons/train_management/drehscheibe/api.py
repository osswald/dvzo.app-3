from base64 import b64decode
from collections import defaultdict
from datetime import datetime
from typing import List
import logging
import os
import requests


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

    def post_day_planning(self, day_planning):
        model = "completed-trip"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        vehicles = defaultdict(lambda: {"km": "0", "railline": []})
        train_records = day_planning.env['train_management.train'].search([
            ('day_planning_id', '=', day_planning.id),
        ])
        for train in train_records:
            train_vehicles = train.train_vehicle
            for train_vehicle in train_vehicles:
                vehicle_info = vehicles[train_vehicle.vehicle.ds_id]
                vehicle_info["railline"].append({
                    "stationStart": train.start_station.short_name,
                    "stationEnd": train.end_station.short_name,
                })
                vehicle_info["km"] +=  train.distance
        vehicle_matrix = [
            {"vehicle": vehicle_id, **info} for vehicle_id, info in vehicles.items()
        ]

        body = {
            "name": day_planning.name,
            "date": day_planning.date.strftime("%d.%m.%Y"),
            "timeStart": "09:00",
            "timeEnd": "18:00",
            "responsiblePerson": "",
            "location": "Bauma",
            "completedDate": datetime.now().strftime("%d.%m.%Y"),
            "completedNote": "Data courtesy by DVZO.app",
            "matrix": vehicle_matrix,
        }
        return self.__post_data(model, body, headers)


if __name__ == "__main__":
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
    drehscheibe = Drehscheibe()
    # drehscheibe.post_day_planning()
