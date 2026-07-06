from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import InventoryTestCommon


@tagged("post_install", "-at_install")
class TestInventory(InventoryTestCommon):
    def test_computed_nr_format(self):
        inventory = self._create_inventory(inventory_nr=42)
        self.assertEqual(inventory.computed_nr, "TT-TP0042")

    def test_computed_nr_unique(self):
        self._create_inventory(inventory_nr=1)
        with self.assertRaises(ValidationError):
            self._create_inventory(inventory_nr=1)

    def test_status_ok_future_expiry(self):
        inventory = self._create_inventory()
        future = fields.Date.today() + timedelta(days=30)
        self._create_check(inventory, future)
        self.assertEqual(inventory.status, self.status_ok)

    def test_status_expired(self):
        inventory = self._create_inventory()
        past = fields.Date.today() - timedelta(days=1)
        self._create_check(inventory, past)
        self.assertEqual(inventory.status, self.status_expired)

    def test_status_no_check(self):
        inventory = self._create_inventory()
        inventory._compute_status_and_latest_expiry_date()
        self.assertEqual(inventory.status, self.status_unavailable)

    def test_latest_check_date(self):
        inventory = self._create_inventory()
        older = fields.Date.today() - timedelta(days=10)
        newer = fields.Date.today() - timedelta(days=1)
        self._create_check(inventory, older + timedelta(days=365), check_date=older)
        self._create_check(inventory, newer + timedelta(days=365), check_date=newer)
        self.assertEqual(inventory.date_calibrated, newer)

    def test_update_inventory_status_cron(self):
        inventory = self._create_inventory(status=self.status_ok.id)
        past = fields.Date.today() - timedelta(days=1)
        self._create_check(inventory, past)
        inventory.write({"status": self.status_ok.id})
        self.env["inventory.inventory"].update_inventory_status()
        self.assertEqual(inventory.status, self.status_expired)

    def test_update_inventory_status_skips_manual_status(self):
        inventory = self._create_inventory(status=self.status_unavailable.id)
        past = fields.Date.today() - timedelta(days=1)
        self._create_check(inventory, past)
        self.env["inventory.inventory"].update_inventory_status()
        self.assertEqual(inventory.status, self.status_unavailable)
