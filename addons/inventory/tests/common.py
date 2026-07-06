from odoo import fields
from odoo.tests.common import TransactionCase


class InventoryTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.inventory_type = cls.env["inventory.type"].create(
            {"name": "Test Type", "short_name": "TT"}
        )
        cls.inventory_place = cls.env["inventory.place"].create(
            {"name": "Test Place", "short_name": "TP"}
        )
        cls.status_ok = cls.env["inventory.status"].create(
            {"name": "OK", "auto_update": True}
        )
        cls.status_expired = cls.env["inventory.status"].create(
            {"name": "Abgelaufen", "auto_update": True}
        )
        cls.status_unavailable = cls.env["inventory.status"].create(
            {"name": "Nicht verfügbar", "auto_update": False}
        )

    def _create_inventory(self, inventory_nr=1, **values):
        data = {
            "name": "Test Item",
            "inventory_nr": inventory_nr,
            "type": self.inventory_type.id,
            "place": self.inventory_place.id,
            "status": self.status_ok.id,
        }
        data.update(values)
        return self.env["inventory.inventory"].create(data)

    def _create_check(self, inventory, expiry_date, check_date=None):
        return self.env["inventory.check"].create(
            {
                "inventory_id": inventory.id,
                "date": check_date or fields.Date.today(),
                "expiry_date": expiry_date,
            }
        )
