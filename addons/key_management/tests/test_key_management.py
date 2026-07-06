from odoo.tests import tagged

from .common import KeyManagementTestCommon


@tagged("post_install", "-at_install")
class TestKeyManagement(KeyManagementTestCommon):
    def test_key_compute_name(self):
        key = self._create_key("42")
        self.assertEqual(key.computed_name, "Main System - Building A - 42")

    def test_key_compute_name_without_group(self):
        key = self.env["key_management.key"].new({"name": "99"})
        key._compute_name()
        self.assertEqual(key.computed_name, "99")

    def test_lending_compute_name(self):
        key = self._create_key("7")
        lending = self.env["key_management.lending"].create(
            {
                "lender": self.lender.id,
                "key": key.id,
            }
        )
        self.assertEqual(lending.computed_name, "7 - Key Lender")

    def test_lending_compute_name_owner_unknown(self):
        key = self._create_key("8")
        lending = self.env["key_management.lending"].create(
            {
                "lender": self.lender.id,
                "key": key.id,
                "owner_unknown": True,
            }
        )
        self.assertEqual(lending.computed_name, "8 - Owner unknown")
