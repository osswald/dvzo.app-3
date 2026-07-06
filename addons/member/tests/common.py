from odoo.tests.common import TransactionCase


class MemberTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department_ops = cls.env["member.department"].create(
            {"name": "Operations"}
        )
        cls.department_board = cls.env["member.department"].create(
            {"name": "Board"}
        )
        cls.type_member = cls.env["member.department_type"].create(
            {"name": "Member", "admin": False}
        )
        cls.type_admin = cls.env["member.department_type"].create(
            {"name": "Admin", "admin": True}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Member Test Partner"})

    def _add_department(self, partner, department, department_type):
        return self.env["member.department_res_partner"].create(
            {
                "person": partner.id,
                "department": department.id,
                "department_type": department_type.id,
            }
        )
