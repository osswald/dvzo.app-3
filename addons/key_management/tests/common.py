from odoo.tests.common import TransactionCase


class KeyManagementTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.key_system = cls.env["key_management.system"].create(
            {
                "short_name": "SYS",
                "name": "Main System",
                "manufacturer": "sea",
            }
        )
        cls.key_group = cls.env["key_management.group"].create(
            {
                "short_name": "GRP",
                "name": "Building A",
                "key_system": cls.key_system.id,
            }
        )
        cls.lender = cls.env["res.partner"].create({"name": "Key Lender"})

    def _create_key(self, number="42", **values):
        data = {
            "name": number,
            "key_group": self.key_group.id,
        }
        data.update(values)
        return self.env["key_management.key"].create(data)
