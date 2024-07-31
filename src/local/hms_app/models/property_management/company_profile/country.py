from odoo import fields, models


class Countries(models.Model):
    _name = "countries"
    _description = "List of Countries"

    name = fields.Char(string="Name", required=True)
