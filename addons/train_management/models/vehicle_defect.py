from ..drehscheibe.api import Drehscheibe
from datetime import datetime
from odoo import models, fields, api
import base64
import requests


class VehicleDefect(models.Model):
    _name = "train_management.vehicle_defect"
    _description = "Vehicle defect"

    vehicle = fields.Many2one("train_management.vehicle", required=True)
    date = fields.Date(required=True, default=datetime.today())
    defectTitle = fields.Char(required=True)
    defectDescription = fields.Text()
    trainNumber = fields.Char()
    whereAtVehicle = fields.Selection(
        selection=[
            ("construction", "construction"),
            ("lighting", "lighting"),
            ("labeling", "labeling"),
            ("brakeSystems", "brakeSystems"),
            ("roof", "roof"),
            ("windowsDoors", "windowsDoors"),
            ("heatingOven", "heatingOven"),
            ("interior", "interior"),
            ("loadArea", "loadArea"),
            ("wheelsAxes", "wheelsAxes"),
            ("seatsBenches", "seatsBenches"),
            ("undercarriage", "undercarriage"),
            ("tensileImpactDevices", "tensileImpactDevices"),
            ("remaining", "remaining"),
        ],
        required=True,
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
        ],
        required=True,
        default="new"
    )
    isAccident = fields.Selection(
        selection=[
            ("no", "no"),
            ("accident", "accident"),
            ("disorder", "disorder"),
            ("endangerment", "endangerment"),
        ],
        required=True,
        default="no"
    )
    isSecurityRelated = fields.Boolean()
    status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("sent_to_ds", "Sent to DS"),
            ("from_ds", "From DS"),
        ],
        required=True,
        default="pending"
    )
    image1 = fields.Image()
    image2 = fields.Image()
    image3 = fields.Image()

def convert_string_date_to_date(string_date, time=None):
    if time:
        return datetime.strptime(
            string_date + " " + time, "%Y-%m-%d %H:%M"
        ).date()
    return datetime.strptime(string_date, "%d.%m.%Y").date()

class VehicleDefectBatchUpdate(models.Model):
    _name = "train_management.vehicle_defect_batch_update"
    _description = "Vehicle Defect Batch Update"

    def update_vehicle_defect_for_single_vehicle(self, drehscheibe, vehicle_id, vehicle_defects):
        existing_defects = self.env["train_management.vehicle_defect"].sudo().search(
            [("vehicle.ds_id", "=", vehicle_id),
             ("status", "=", "from_ds")
            ]
        )
        existing_defects.unlink()
        for old_item in vehicle_defects:
            new_item = {}
            new_item["date"] = convert_string_date_to_date(old_item.get("date"))
            new_item["defectTitle"] = old_item.get("defectTitle")
            new_item["defectDescription"] = old_item.get("defectDescription")
            new_item["trainNumber"] = old_item.get("trainNumber")
            new_item["whereAtVehicle"] = old_item.get("whereAtVehicle", "remaining")
            new_item["isAccident"] = old_item.get("isAccident", "no")
            new_item["isSecurityRelated"] = old_item.get("isSecurityRelated")
            new_item["status"] = "from_ds"
            len_images = (len(old_item.get("images", []))
                          if len(old_item.get("images", [])) <= 3
                          else 3)
            for i in range(0, len_images):
                prod_url = "drehscheibe.hech.ch"
                dev_url = "drehscheibe.e9li.com"
                url = old_item.get("images")[i].replace(dev_url, prod_url)
                response = requests.get(url)
                response.raise_for_status()
                image = base64.b64encode(response.content)
                new_item[f"image{i+1}"] = image
            new_item["vehicle"] = self.env["train_management.vehicle"].sudo().search(
                [("ds_id", "=", vehicle_id)]
            ).id
            self.env["train_management.vehicle_defect"].sudo().create(new_item)

    def send_new_defects2ds(self):
        new_defects = self.env["train_management.vehicle_defect"].sudo().search(
            [("status", "=", "pending")]
        )
        drehscheibe = Drehscheibe()
        for defect in new_defects:
            drehscheibe.post_vehicle_defects(defect)
            defect.unlink()

    def update_all_vehicle_defects(self):
        vehicle_ids = self.env[
            "train_management.vehicle"].sudo().search([]).mapped("ds_id")
        vehicle_ids = [x for x in vehicle_ids if x]
        drehscheibe = Drehscheibe()

        from multiprocessing.pool import ThreadPool
        with ThreadPool(processes=10) as pool:
            vehicle_defects = pool.map(drehscheibe.get_vehicle_defects, vehicle_ids)

        for vehicle_id, defects in vehicle_defects:
            self.update_vehicle_defect_for_single_vehicle(
                drehscheibe, vehicle_id, defects)

    @api.model
    def update_vehicle_defect(self):
        self.send_new_defects2ds()
        self.update_all_vehicle_defects()
